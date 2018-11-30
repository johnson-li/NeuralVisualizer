using System;
using System.IO;
using UnityEngine;

namespace TensorAR
{
    public class Utils
    {
        public static BinaryReader LoadBinary(String str)
        {
            var asset = Resources.Load(str) as TextAsset;
            Stream s = new MemoryStream(asset.bytes);
            var br = new BinaryReader(s);
            return br;
        }


        public static Sprite Bytes2Sprite(byte[] bytes, int width, int height)
        {
            var text = new Texture2D(width, height, TextureFormat.RGBA32, false);
            text.LoadRawTextureData(bytes);
            text.Apply();
            var sprite = Sprite.Create(text, new Rect(0, 0, text.width, text.height), new Vector2(.5f, .5f));
            return sprite;
        }
    }
}