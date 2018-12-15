//-----------------------------------------------------------------------
// <copyright file="AugmentedImageExampleController.cs" company="Google">
//
// Copyright 2018 Google Inc. All Rights Reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
// http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
//
// </copyright>
//-----------------------------------------------------------------------

namespace TensorAR
{
    using System.Collections.Generic;
    using System.Runtime.InteropServices;
    using HuaweiARUnitySDK;
    using UnityEngine;
    using HuaweiARInternal;
    using UnityEngine.UI;

    public class AugmentedController : MonoBehaviour
    {
        public ImageCloud imageCloudPrototype;

        public GameObject FitToScanOverlay;

        private Dictionary<int, ImageCloud> imageClouds = new Dictionary<int, ImageCloud>();

        private List<ARAugmentedImage> augmentedImages = new List<ARAugmentedImage>();

        public void Update()
        {
            if (ARFrame.GetTrackingState() != ARTrackable.TrackingState.TRACKING)
            {
                ARDebug.LogInfo("GetTrackingState no tracing return <<");
                return;
            }

            ARFrame.GetTrackables(augmentedImages, ARTrackableQueryFilter.UPDATED);
            ARDebug.LogInfo("m_TempAugmentedImages size {0}", augmentedImages.Count);

            // Create visualizers and anchors for updated augmented images that are tracking and do not previously
            // have a visualizer. Remove visualizers for stopped images.
            foreach (var image in augmentedImages)
            {
                ImageCloud imageCloud;
                imageClouds.TryGetValue(image.GetDataBaseIndex(), out imageCloud);

                ARDebug.LogInfo("GetTrackingState {0}", image.GetTrackingState());
                if (image.GetTrackingState() == ARTrackable.TrackingState.TRACKING && imageCloud != null)
                {
                    imageCloud.image = image;
                }

                if (image.GetTrackingState() == ARTrackable.TrackingState.TRACKING && imageCloud == null)
                {
                    imageCloud = Instantiate(imageCloudPrototype, image.GetCenterPose().position,
                        image.GetCenterPose().rotation);
                    ARDebug.LogInfo("create position {0} rotation {1}", image.GetCenterPose().position,
                        image.GetCenterPose().rotation);
                    imageCloud.image = image;
                    imageClouds.Add(image.GetDataBaseIndex(), imageCloud);
                }
                else if (image.GetTrackingState() == ARTrackable.TrackingState.STOPPED && imageCloud != null)
                {
                    imageClouds.Remove(image.GetDataBaseIndex());
                    GameObject.Destroy(imageCloud.gameObject);
                }
            }

            // Show the fit-to-scan overlay if there are no images that are Tracking.
            foreach (var visualizer in imageClouds.Values)
            {
                if (visualizer.image.GetTrackingState() == ARTrackable.TrackingState.TRACKING)
                {
                    FitToScanOverlay.SetActive(false);
                    return;
                }
            }

            FitToScanOverlay.SetActive(true);
        }
    }
}