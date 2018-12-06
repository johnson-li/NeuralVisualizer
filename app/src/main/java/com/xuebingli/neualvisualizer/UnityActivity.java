package com.xuebingli.neualvisualizer;

import android.os.Bundle;

import com.xuebingli.proto.Algorithm;
import com.xuebingli.proto.Dataset;
import com.xuebingli.proto.ReduceRequest;
import com.xuebingli.tensorar.UnityPlayerActivity;

import java.lang.ref.WeakReference;

import javax.inject.Inject;

import dagger.android.AndroidInjection;
import io.grpc.ManagedChannel;

public class UnityActivity extends UnityPlayerActivity {

  public float[][] points;
  public boolean initiated;
  @Inject public ManagedChannel channel;

  @Override
  protected void onCreate(Bundle savedInstanceState) {
    AndroidInjection.inject(this);
    super.onCreate(savedInstanceState);
  }

  public void reduceDimension() {
    ReduceRequest request =
        ReduceRequest.newBuilder()
            .setAlgorithm(Algorithm.TSNE)
            .setDataset(Dataset.MNIST)
            .setNumber(300)
            .setDimention(3)
            .build();

    points = new float[request.getNumber()][];
    new DimReductionTask(new WeakReference(this), channel, request).execute();
  }
}
