package injection

import com.xuebingli.neualvisualizer.MainActivity
import com.xuebingli.neualvisualizer.UnityActivity
import dagger.Module
import dagger.android.ContributesAndroidInjector

@Module
abstract class ActivityBuilder {
    @ContributesAndroidInjector
    abstract fun bindMainActivity(): MainActivity

    @ContributesAndroidInjector
    abstract fun bindUnityActivity(): UnityActivity
}