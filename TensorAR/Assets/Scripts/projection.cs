using System;
using TensorAR;
using UnityEngine;

public class Projection : MonoBehaviour
{
    private static int ROWS = 28;
    private static int COLS = 28;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Escape))
        {
            Application.Quit();
        }

//        transform.Translate(Time.deltaTime, Time.deltaTime, Time.deltaTime);
    }

    private void Awake()
    {
        DrawImages(1000);
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

    private byte[] LoadTrainLabels(int number)
    {
        var trainLabel = Utils.LoadBinary("MNIST/train-labels-idx1-ubyte");
        var magic = trainLabel.ReadUInt32();
        Debug.Assert(magic == 0x00000801);
        var num = trainLabel.ReadInt32();
        var labels = trainLabel.ReadBytes(number);
        return labels;
    }

    private void DrawImages(int number)
    {
        var images = LoadTrainImages(number);
        var labels = LoadTrainLabels(number);
        for (int i = 0; i < number; i++)
        {
            var image = new GameObject(String.Format("image-{0}", i), typeof(SpriteRenderer));
            var transform = image.GetComponent<Transform>();
            transform.position = new Vector3(i / 10 % 10, i % 10, i / 100 + 5);
//            transform.localScale = new Vector3(4, 4, 4);
            transform.rotation = new Quaternion(180, 0, 0, 1);
            var sprite = Utils.Bytes2Sprite(images[i], ROWS, COLS);
            image.GetComponent<SpriteRenderer>().sprite = sprite;
//            Debug.LogWarning(BitConverter.ToString(sprite.texture.GetRawTextureData()));
        }
    }
}