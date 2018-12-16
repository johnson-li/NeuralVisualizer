package com.xuebingli.neualvisualizer;

import android.os.Bundle;
import android.util.Log;

import com.pixplicity.easyprefs.library.Prefs;
import com.xuebingli.proto.Algorithm;
import com.xuebingli.proto.Dataset;
import com.xuebingli.proto.ReduceGrpc;
import com.xuebingli.proto.ReduceReply;
import com.xuebingli.proto.ReduceRequest;
import com.xuebingli.tensorar.UnityPlayerActivity;

import java.util.ArrayList;
import java.util.List;

import javax.inject.Inject;

import dagger.android.AndroidInjection;
import io.grpc.ManagedChannel;
import io.grpc.stub.StreamObserver;

public class UnityActivity extends UnityPlayerActivity {

  public static final int MAX_ITERATION = 1000;
  public List<float[][]> points = new ArrayList<>();
  public int iteration = -1;
  @Inject public ManagedChannel channel;
  private boolean showLabel;
  private int labelNumber;
  private int imageNumber;
  private int dimensions;

  {
    for (int i = 0; i < MAX_ITERATION; i++) {
      points.add(null);
    }
  }

  @Override
  protected void onCreate(Bundle savedInstanceState) {
    AndroidInjection.inject(this);
    super.onCreate(savedInstanceState);

    showLabel = Prefs.getBoolean(Cons.SHOW_LABEL, true);
    labelNumber = Prefs.getInt(Cons.LABEL_NUMBER, 10);
    imageNumber = Prefs.getInt(Cons.IMAGE_NUMBER, 100);
    dimensions = Prefs.getInt(Cons.DIMENSION, 3);
  }

  public float[][] getPoints(int iteration) {
    return points.get(iteration);
  }

  public void reduceDimension() {
    ReduceRequest request =
        ReduceRequest.newBuilder()
            .setAlgorithm(Algorithm.TSNE)
            .setDataset(Dataset.MNIST)
            .setLabelNumber(labelNumber)
            .setImageNumber(imageNumber)
            .setDimention(3)
            .build();

    ReduceGrpc.ReduceStub stub = ReduceGrpc.newStub(channel);
    stub.reduceDimention(
        request,
        new StreamObserver<ReduceReply>() {
          @Override
          public void onNext(ReduceReply value) {
            Log.d("iteration", "Iteration: " + value.getIteration());
            float[][] data = new float[value.getPoints3Count()][3];
            for (int i = 0; i < value.getPoints3Count(); i++) {
              data[i][0] = value.getPoints3(i).getX();
              data[i][1] = value.getPoints3(i).getY();
              data[i][2] = value.getPoints3(i).getZ();
            }
            points.set(value.getIteration(), data);
            iteration = value.getIteration();
          }

          @Override
          public void onError(Throwable t) {
            Log.e("error", t.getMessage());
          }

          @Override
          public void onCompleted() {}
        });
  }
}
