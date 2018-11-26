package com.xuebingli.neualvisualizer

import android.content.Intent
import android.os.Bundle
import android.support.v7.app.AppCompatActivity
import android.view.View
import com.huawei.hiar.ARSession
import com.xuebingli.tensorar.UnityPlayerActivity
import kotlinx.android.synthetic.main.activity_main.*
import java.util.logging.Logger

class MainActivity : AppCompatActivity() {

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        setSupportActionBar(toolbar)

        Logger.getLogger("SDK version: " + MainActivity::class.java.name).warning(ARSession.CURRENT_SDK_VERSIONCODE.toString())
    }

    fun click(view: View) {
        val intent = Intent(baseContext, UnityPlayerActivity::class.java)
        startActivity(intent)
    }
}
