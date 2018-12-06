package com.xuebingli.neualvisualizer

import android.content.Context
import android.os.AsyncTask
import android.util.Log
import com.xuebingli.proto.ReduceGrpc
import com.xuebingli.proto.ReduceReply
import com.xuebingli.proto.ReduceRequest
import io.grpc.ManagedChannel
import java.lang.ref.WeakReference

class DimReductionTask(var context: WeakReference<Context>, val channel: ManagedChannel,
                       val request: ReduceRequest) : AsyncTask<ReduceRequest, Void, ReduceReply>() {
    override fun doInBackground(vararg params: ReduceRequest?): ReduceReply {
        val reduceService = ReduceGrpc.newBlockingStub(channel)
        return reduceService.reduceDimention(request)
    }

    override fun onPreExecute() {
        Log.d("point cloud", "starting DimReductionTask")
    }

    override fun onPostExecute(result: ReduceReply?) {
        result!!.points3List.forEachIndexed { index, point3D ->
            val point = floatArrayOf(.1f)
            point[0] = point3D.x
            point[1] = point3D.y
            point[2] = point3D.z
            (context.get() as UnityActivity).points[index] = point
        }
        (context.get() as UnityActivity).initiated = true
        Log.d("point cloud", result.toString())
    }
}