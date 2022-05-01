# Glootie's App
**Category:** reverse,pwn

**Author:** En3rRe

## Description

Apparently Jerry doesn't know how to read the warnings! Do you ?

## Solution
<details>
 <summary>Reveal Spoiler</summary>
 First, we need to inspect the app and check what is doing. We can run the app on an emulator and we see that there is a login screen. Since this is a reverse challenge let's try to reverse the apk. Two instances of the same app were given with the one having the name the app_debug.apk so let's start with that. 

Let's reverse the app using the JADX. Jadx has a GUI and also has a Java decompiler. 


By looking at the Manifest there are 3 activities. So the app should be straightforward. We can look at the main activity. 

There is an interesting method called getFlag. Let's see how we can invoke it. It seems if we make the Integer.parseInt failed there is an exception that is thrown and the getFlag is invoked in the catch statement. All we need to do is to enter a password that is not a string. 

If we do that nothing happens on the emulator. If we look closely the flag is written in the logs. We need to get the logs from the emulator.

Let's start an adp shell and get a look at the app logs using logcat. First, we need the pid of the app that is running on the emulator.

 `adb shell ps |grep "ctf"`

Now we are going to use logcat to capture the logs. 
 `adb shell logcat | grep $PID `

At the end of the last Error log there is `ccsc{flag1_` However this is a placeholder let's do the same with the app_release. 

Repeating the same process with app_release.apk gives you `ccsc{ch3ck_l0g5`.

Okay, let's move on. The goal now it's to get past the login Activity to the next one. However, you have to guess a SecureRandom Int. This is not possible. If we check the manifest there is one more activity that is exported. Therefore we can exploit that to get into that without providing credentials. 

All we have to do is : 
 
`adb shell am start -n com.example.ctf_challenge/.GotIn` 

This is forcing the app to start on the other extern activity. Let's look at the code one more time. The GotIn Activity is just registering a new BroadcastReceiver, AirplaneModeChangeReceiver. Let's check the code there. It seems that if the Airplane mode is on and you give an extra string it starts the final Activity that is called Broadcast. It expects a key pair value with the AirplaneMode change event, with `j3rrY` as a key and `D0N0tD3vElOpTh3App` as a value. 

`adb shell`
`su`
`am broadcast -a android.intent.action.AIRPLANE_MODE --es j3rrY D0N0tD3vElOpTh3App`

Now there is a final screen. The button seems that is not doing anything. However, if we look carefully at the code of the Activity Broadcast it seems that is broadcasting an intent with the flag. We need a way to listen for that intent. 

We can do that using drozer-agent. Drozer agent is an attacking apk developed from F-secure that can help you with multiple attacking scenarios. It has the apk and also the server that you use to control the apk. We can download the apk from https://github.com/mwrlabs/drozer/releases/download/2.3.4/drozer-agent-2.3.4.apk. 


We also need to forward the default port drozer is using to our computer from the emulator using
`adb forward tcp:31415 tcp:31415`

We install the apk on the emulator and we also spawn the docker server.
`docker run -it fsecurelabs/drozer` 
Then we connect to the apk using 
`drozer console connect --server host.docker.internal` 

Now the final part set up a listener. 

`run app.broadcast.sniff --action com.example.ctf_challenge.OUT`

Press the button and here is the second part of the flag:
`_aNd_l1st3n}`

    FLAG: `ccsc{ch3ck_l0g5_aNd_l1st3n}`
</details>
