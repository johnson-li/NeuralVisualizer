package com.xuebingli.neualvisualizer

import android.content.Intent
import android.os.Bundle
import android.view.Menu
import android.view.MenuInflater
import android.view.MenuItem
import android.view.View
import android.widget.Toast
import com.xuebingli.tensorar.UnityPlayerActivity
import dagger.android.support.DaggerAppCompatActivity
import io.grpc.ManagedChannel
import io.grpc.examples.helloworld.GreeterGrpc
import io.grpc.examples.helloworld.HelloRequest
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
        val intent = Intent(baseContext, UnityPlayerActivity::class.java)
        startActivity(intent)
    }

    private fun test() {
        val message = HelloRequest.newBuilder().setName("hella").build()
        val greeterService = GreeterGrpc.newBlockingStub(channel)
        val reply = greeterService.sayHello(message)
        Toast.makeText(this, reply.message, Toast.LENGTH_SHORT).show()
    }

    override fun onCreateOptionsMenu(menu: Menu): Boolean {
        val inflater: MenuInflater = menuInflater
        inflater.inflate(R.menu.menu_main, menu)
        return true
    }

    override fun onOptionsItemSelected(item: MenuItem): Boolean {
        // Handle item selection
        return when (item.itemId) {
            R.id.test -> {
                test()
                true
            }
            else -> super.onOptionsItemSelected(item)
        }
    }
}
