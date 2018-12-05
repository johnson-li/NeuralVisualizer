using System;
using System.Collections;
using System.Collections.Generic;
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

    private void Awake()
    {
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
    }

    public void Update()
    {
        if (image == null || image.GetTrackingState() != ARTrackable.TrackingState.TRACKING)
        {
            return;
        }

        var width = image.GetExtentX();
        var height = image.GetExtentZ();
        if (AREnginesSelector.Instance.GetCreatedEngine() == AREnginesType.HUAWEI_AR_ENGINE)
        {
            ARDebug.LogInfo("showing points");
            for (int i = 0; i < points.Length; i++)
            {
                var point = points[i];
                point.transform.position = image.GetCenterPose().position;
                point.transform.localScale = new Vector3(.1f, .1f, .1f);
                var rotation = image.GetCenterPose().rotation;
                point.transform.rotation = rotation;
                var sprite = Utils.Bytes2Sprite(images[i], ROWS, COLS);
                point.GetComponent<SpriteRenderer>().sprite = sprite;
            }
        }
    }
}