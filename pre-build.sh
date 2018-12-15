#!/usr/bin/env bash

cd "$(dirname "$0")"

gradle_file=TensorAR/Android/TensorAR/build.gradle
sed -i -e 's/com\.android\.application/com.android.library/g' ${gradle_file}
sed -i -e '/applicationId/d' ${gradle_file}

pass=`grep allprojects ${gradle_file} -A2|grep google > /dev/null; echo $?`
if [[ "$pass" = '1' ]]
then
line=`grep -n allprojects ${gradle_file}|cut -f1 -d:`
sed -i -e "$((line+1))a\\
\ \ \ \ \ \ \ \ google()\\
\ \ \ \ \ \ \ \ jcenter()\\
" ${gradle_file}
fi

manifest_file=TensorAR/Android/TensorAR/src/main/AndroidManifest.xml
sed -i -e '/intent-filter/d' ${manifest_file}
sed -i -e '/android\.intent\.action\.MAIN/d' ${manifest_file}
sed -i -e '/android\.intent\.category\.LAUNCHER/d' ${manifest_file}

cd TensorAR/Android/TensorAR
./gradlew build
