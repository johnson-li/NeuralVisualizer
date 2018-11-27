package injection

import com.xuebingli.neualvisualizer.NeuralApplication
import dagger.BindsInstance
import dagger.Component
import dagger.android.AndroidInjectionModule
import dagger.android.support.AndroidSupportInjectionModule
import javax.inject.Singleton

@Singleton
@Component(modules = [NeuralModule::class, AndroidSupportInjectionModule::class, ActivityBuilder::class])
interface NeuralComponent {

    @Component.Builder
    interface Builder {
        @BindsInstance
        fun application(application: NeuralApplication): Builder

        fun build(): NeuralComponent
    }

    fun inject(app: NeuralApplication)
}