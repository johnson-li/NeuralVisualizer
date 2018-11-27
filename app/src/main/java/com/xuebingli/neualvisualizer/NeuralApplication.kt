package com.xuebingli.neualvisualizer

import android.app.Activity
import android.app.Application
import dagger.android.AndroidInjector
import dagger.android.DispatchingAndroidInjector
import dagger.android.HasActivityInjector
import injection.DaggerNeuralComponent
import injection.NeuralComponent
import javax.inject.Inject


class NeuralApplication : Application(), HasActivityInjector {

    @Inject
    lateinit var activityDispatchingAndroidInjector: DispatchingAndroidInjector<Activity>

    override fun activityInjector(): AndroidInjector<Activity> = activityDispatchingAndroidInjector

    lateinit var component: NeuralComponent

    override fun onCreate() {
        super.onCreate()
        DaggerNeuralComponent.builder().application(this).build().inject(this)
    }
}