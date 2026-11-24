set -e
cd ~/workspace/apk-mod/new2
T=$HOME/workspace/apk-mod/tools
export PATH=$T/jdk-17.0.21.1+2/bin:$T/android-14:$PATH
which zip unzip >/dev/null
rm -rf build && mkdir build && cp new.apk build/mod.apk
cd build
unzip -l mod.apk 'META-INF/*' | awk '{print $4}' | grep -E '\.(SF|RSA|DSA|EC|MF)$' > sigs.txt || true
cat sigs.txt
[ -s sigs.txt ] && zip -q -d mod.apk $(cat sigs.txt)
mkdir -p stage && cp ../decoded_r/resources.arsc stage/
(cd stage && zip -q -0 ../mod.apk resources.arsc)
zipalign -f -p 4 mod.apk aligned.apk
if [ ! -f ../sohel_ig.jks ]; then
  head -c 24 /dev/urandom | base64 | tr -dc A-Za-z0-9 > ../.kspass
  keytool -genkeypair -keystore ../sohel_ig.jks -alias sohel -keyalg RSA -keysize 2048 -validity 10000 -storepass "$(cat ../.kspass)" -keypass "$(cat ../.kspass)" -dname "CN=Sohel" >/dev/null 2>&1
  chmod 600 ../.kspass ../sohel_ig.jks
fi
apksigner sign --ks ../sohel_ig.jks --ks-pass file:../.kspass --ks-key-alias sohel --out Sohel_IG_456_arm64.apk aligned.apk
apksigner verify Sohel_IG_456_arm64.apk && echo VERIFIED
aapt dump badging Sohel_IG_456_arm64.apk | grep -E "^package|application-label|native-code"
ls -la Sohel_IG_456_arm64.apk
