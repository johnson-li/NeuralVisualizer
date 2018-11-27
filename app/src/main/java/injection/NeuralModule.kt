package injection

import android.content.Context
import com.xuebingli.neualvisualizer.BuildConfig
import com.xuebingli.neualvisualizer.NeuralApplication
import dagger.Module
import dagger.Provides
import io.grpc.ManagedChannel
import io.grpc.ManagedChannelBuilder
import javax.inject.Singleton

@Module
class NeuralModule {
    @Provides
    @Singleton
    fun provideApplication(app: NeuralApplication): Context = app

    @Provides
    @Singleton
    fun provideChannel(): ManagedChannel {
        return ManagedChannelBuilder.forAddress(BuildConfig.ServerIP, BuildConfig.ServerPort).usePlaintext().build()
    }
}