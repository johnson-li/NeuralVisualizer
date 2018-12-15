package com.xuebingli.neualvisualizer

import android.content.Intent
import android.os.Bundle
import android.view.Menu
import android.view.MenuInflater
import android.view.MenuItem
import android.view.View
import android.widget.Toast
import com.xuebingli.proto.Algorithm
import com.xuebingli.proto.Dataset
import com.xuebingli.proto.ReduceGrpc
import com.xuebingli.proto.ReduceRequest
import dagger.android.support.DaggerAppCompatActivity
import io.grpc.ManagedChannel
import kotlinx.android.synthetic.main.activity_main.*
import javax.inject.Inject

class MainActivity : DaggerAppCompatActivity() {

    @Inject
    lateinit var channel: ManagedChannel

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        setSupportActionBar(toolbar)
    }

    fun click(view: View) {
        val intent = Intent(baseContext, UnityActivity::class.java)
        startActivity(intent)
    }

    private fun test() {
        val request = ReduceRequest.newBuilder().setNumber(100).setDimention(3)
                .setDataset(Dataset.MNIST).setAlgorithm(Algorithm.TSNE).build()
        val reduceService = ReduceGrpc.newBlockingStub(channel)
        val reply = reduceService.reduceDimention(request)
        Toast.makeText(this, reply.points3List.toString(), Toast.LENGTH_SHORT).show()
    }


    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        val inflater: MenuInflater = menuInflater
        inflater.inflate(R.menu.menu_main, menu)
        return true
    }

    private fun reduceDimension() {
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        // Handle item selection
        return when (item.itemId) {
            R.id.test -> {
                test()
                true
            }
            R.id.reduce_dimension -> {
                reduceDimension()
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }

}
