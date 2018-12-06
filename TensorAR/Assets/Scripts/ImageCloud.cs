using System;
using System.Collections;
using System.Collections.Generic;
using System.Linq;
using HuaweiARInternal;
using HuaweiARUnitySDK;
using TensorAR;
using UnityEngine;

public class ImageCloud : MonoBehaviour
{
    public ARAugmentedImage image;
    private static int ROWS = 28;
    private static int COLS = 28;
    private GameObject[] points;
    private byte[][] images;
    private static int POINT_NUMBER = 50;
    private AndroidJavaClass unityPlayer;
    private AndroidJavaObject activity;
    private List<float[]> pointsLocation = new List<float[]>();

    private void Awake()
    {
        unityPlayer = new AndroidJavaClass("com.unity3d.player.UnityPlayer");
        activity = unityPlayer.GetStatic<AndroidJavaObject>("currentActivity");
        DrawImages(POINT_NUMBER);
    }

    private byte[][] LoadTrainImages(int number)
    {
        var trainImage = Utils.LoadBinary("MNIST/train-images-idx3-ubyte");
        var magic = trainImage.ReadInt32();
        Debug.Assert(magic == 0x00000803);
        var num = trainImage.ReadInt32();
        var rows = trainImage.ReadInt32();
        var cols = trainImage.ReadInt32();
        Debug.Assert(rows == ROWS);
        Debug.Assert(cols == COLS);
        var images = new byte[number][];
        for (var i = 0; i < number; i++)
        {
            images[i] = new byte[rows * cols * 4];
            var image = trainImage.ReadBytes(rows * cols);
            for (int r = 0; r < rows; r++)
            {
                for (int c = 0; c < cols; c++)
                {
                    var k = r * cols + c;
                    images[i][4 * k] = 0xff;
                    images[i][4 * k + 1] = 0xff;
                    images[i][4 * k + 2] = 0xff;
                    images[i][4 * k + 3] = image[k];
                }
            }
        }

        return images;
    }


    private void DrawImages(int number)
    {
        images = LoadTrainImages(number);
        points = new GameObject[POINT_NUMBER];
        for (var i = 0; i < POINT_NUMBER; i++)
        {
            points[i] = new GameObject(String.Format("image-{0}", i), typeof(SpriteRenderer));
        }

        ARDebug.LogInfo("reduce dimension");
        activity.Call("reduceDimension", new object[0]);
    }

    public void Update()
    {
        if (image == null || image.GetTrackingState() != ARTrackable.TrackingState.TRACKING)
        {
            return;
        }

        var initiated = activity.Get<bool>("initiated");
        if (initiated && !pointsLocation.Any())
        {
            var obj = activity.Get<AndroidJavaObject>("points");
            var array = AndroidJNIHelper.ConvertFromJNIArray<AndroidJavaObject[]>(obj.GetRawObject());
            foreach (AndroidJavaObject item in array)
            {
                var tuple = AndroidJNIHelper.ConvertFromJNIArray<float[]>(item.GetRawObject());
                pointsLocation.Add(tuple);
            }

            ARDebug.LogInfo("init points location: " + pointsLocation.Count);
        }

        ARDebug.LogInfo(pointsLocation.ToString());

        var width = image.GetExtentX() * 1.5f;
        var height = image.GetExtentZ() * 1.5f;
        if (AREnginesSelector.Instance.GetCreatedEngine() == AREnginesType.HUAWEI_AR_ENGINE)
        {
            ARDebug.LogInfo("showing points, fix: " + pointsLocation.Any());
            for (int i = 0; i < points.Length; i++)
            {
                var point = points[i];
                var position = image.GetCenterPose().position;
                var rotation = image.GetCenterPose().rotation;
                rotation.y += 180;
                rotation.x += 90;
                if (pointsLocation.Any())
                {
                    var fix = pointsLocation[i];
                    position.x += width * fix[0] - width / 2;
                    position.z += height * fix[2] - height / 2;
                    position.y += fix[1] / 2;
                }

                point.transform.position = position;
                point.transform.localScale = new Vector3(.1f, .1f, .1f);
                point.transform.rotation = rotation;
                var sprite = Utils.Bytes2Sprite(images[i], ROWS, COLS);
                point.GetComponent<SpriteRenderer>().sprite = sprite;
            }
        }
    }
}