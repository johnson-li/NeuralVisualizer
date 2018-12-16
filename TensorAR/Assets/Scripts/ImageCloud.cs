using System;
using System.Collections.Generic;
using System.Linq;
using HuaweiARInternal;
using HuaweiARUnitySDK;
using TensorAR;
using UnityEngine;
using UnityEngine.UI;

public class ImageCloud : MonoBehaviour
{
    public ARAugmentedImage image;
    public GameObject FirstPersonCamera;
    [SerializeField] private Sprite circleSprite;
    private static int ROWS = 28;
    private static int COLS = 28;
    private bool showLabel = true;
    private int labelNumber;
    private int imageNumber;
    private GameObject[] points;
    private byte[][] images;
    private int maxIteration = -1;
    private AndroidJavaClass unityPlayer;
    private AndroidJavaObject activity;
    private List<float[]> pointsLocation = new List<float[]>();
    private float scale = 100;

    private void Awake()
    {
        FirstPersonCamera = GameObject.Find("First Person Camera");
        unityPlayer = new AndroidJavaClass("com.unity3d.player.UnityPlayer");
        activity = unityPlayer.GetStatic<AndroidJavaObject>("currentActivity");
        DrawImages();
    }

    private byte[][] LoadTrainImages()
    {
        var indexes = new int[10];
        var trainImage = Utils.LoadBinary("MNIST/train-images-idx3-ubyte");
        var trainLabel = Utils.LoadBinary("MNIST/train-labels-idx1-ubyte");
        var magic = trainImage.ReadInt32();
        Debug.Assert(magic == 0x00000803);
        magic = trainLabel.ReadInt32();
        Debug.Assert(magic == 0x00000801);
        var num = trainImage.ReadInt32();
        num = trainLabel.ReadInt32();
        var rows = trainImage.ReadInt32();
        var cols = trainImage.ReadInt32();
        Debug.Assert(rows == ROWS);
        Debug.Assert(cols == COLS);
        var images = new byte[labelNumber * imageNumber][];
        for (var i = 0; i < images.Length;)
        {
            var img = trainImage.ReadBytes(rows * cols);
            var label = trainLabel.ReadByte();
            if (label >= labelNumber || indexes[label] >= imageNumber)
            {
                continue;
            }

            var index = label * imageNumber + indexes[label]++;
            images[index] = new byte[rows * cols * 4];
            for (int r = 0; r < rows; r++)
            {
                for (int c = 0; c < cols; c++)
                {
                    var k = r * cols + c;
                    images[index][4 * k] = 0xff;
                    images[index][4 * k + 1] = 0xff;
                    images[index][4 * k + 2] = 0xff;
                    images[index][4 * k + 3] = img[(rows - r - 1) * cols + c];
                }
            }

            i++;
        }

        return images;
    }


    private void DrawImages()
    {
        showLabel = activity.Get<bool>("showLabel");
        imageNumber = activity.Get<int>("imageNumber");
        labelNumber = activity.Get<int>("labelNumber");
        images = LoadTrainImages();
        points = new GameObject[imageNumber * labelNumber];
        for (var i = 0; i < points.Length; i++)
        {
            points[i] = new GameObject(String.Format("image-{0}", i), typeof(SpriteRenderer));
            var sprite = Utils.Bytes2Sprite(images[i], ROWS, COLS);
            if (!showLabel)
            {
//                sprite = Resources.Load();
            }

            points[i].GetComponent<SpriteRenderer>().sprite = sprite;
        }

        activity.Call("reduceDimension", new object[0]);
    }

    public void updatePoints()
    {
        if (image == null || image.GetTrackingState() != ARTrackable.TrackingState.TRACKING)
        {
            return;
        }

        var iteration = activity.Get<int>("iteration");
        if (iteration > maxIteration)
        {
            ARDebug.LogInfo("iteration: " + iteration);
            maxIteration = iteration;
            pointsLocation.Clear();
            var obj = activity.Call<AndroidJavaObject>("getPoints", new object[] {iteration});
            var array = AndroidJNIHelper.ConvertFromJNIArray<AndroidJavaObject[]>(obj.GetRawObject());
            foreach (AndroidJavaObject item in array)
            {
                var tuple = AndroidJNIHelper.ConvertFromJNIArray<float[]>(item.GetRawObject());
                pointsLocation.Add(tuple);
                item.Dispose();
            }

            obj.Dispose();

            GameObject.Find("Iteration").GetComponent<Text>().text = "Iteration: " + iteration;
        }

        ARDebug.LogInfo("points location: " + pointsLocation);

        var width = image.GetExtentX() * scale / 100;
        var height = image.GetExtentZ() * scale / 100;
        if (AREnginesSelector.Instance.GetCreatedEngine() == AREnginesType.HUAWEI_AR_ENGINE)
        {
            ARDebug.LogInfo("showing points, fix: " + pointsLocation.Any());
            for (int i = 0; i < points.Length; i++)
            {
                var point = points[i];
                var position = image.GetCenterPose().position;
                var rotation = image.GetCenterPose().rotation;
                if (pointsLocation.Any())
                {
                    var fix = pointsLocation[i];
                    position.x += width * fix[0] - width / 2;
                    position.z += height * fix[2] - height / 2;
                    position.y += fix[1] * scale / 300 + .05f;
                }

                rotation = FirstPersonCamera.transform.rotation;
//                rotation = new Quaternion(rotation.x + 180, rotation.y, rotation.z, rotation.w);

                point.transform.position = position;
                point.transform.localScale = new Vector3(.05f, .05f, .05f);
                point.transform.rotation = rotation;
            }
        }
    }

    private void updateZoom()
    {
        if (Input.touchCount == 2)
        {
            Touch touchZero = Input.GetTouch(0);
            Touch touchOne = Input.GetTouch(1);
            Vector2 touchZeroPrevPos = touchZero.position - touchZero.deltaPosition;
            Vector2 touchOnePrevPos = touchOne.position - touchOne.deltaPosition;
            float prevTouchDeltaMag = (touchZeroPrevPos - touchOnePrevPos).magnitude;
            float touchDeltaMag = (touchZero.position - touchOne.position).magnitude;
            float deltaMagnitudeDiff = prevTouchDeltaMag - touchDeltaMag;
            if (scale - deltaMagnitudeDiff > 0)
            {
                scale -= deltaMagnitudeDiff;
            }
        }
    }

    public void Update()
    {
        updateZoom();
        updatePoints();
    }
}