package com.example.iotmqtt;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.TextView;

import com.example.iotmqtt.helpers.MQTTHelper;

import org.eclipse.paho.client.mqttv3.IMqttDeliveryToken;
import org.eclipse.paho.client.mqttv3.MqttCallbackExtended;
import org.eclipse.paho.client.mqttv3.MqttException;
import org.eclipse.paho.client.mqttv3.MqttMessage;

public class MainActivity extends AppCompatActivity implements View.OnClickListener {
    MQTTHelper mqttHelper;

    TextView dataTemp;
    TextView dataLed;
    TextView dataDoor;

    final String subscriptionTopic = "temperature";
    final String subscriptionTopic2 = "leds";
    final String subscriptionTopic3 = "doorbell";



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        findViewById(R.id.ledBtn).setOnClickListener(this);

        dataTemp = findViewById(R.id.textTemp);
        dataLed  = findViewById(R.id.textLed);
        dataDoor = findViewById(R.id.textDoor);

        mqttHelper = new MQTTHelper((getApplicationContext()));

        startMqtt();
    }

    private void startMqtt(){
       // mqttHelper = new MQTTHelper((getApplicationContext()));
        mqttHelper.setCallback(new MqttCallbackExtended() {
            @Override
            public void connectComplete(boolean reconnect, String serverURI) {

            }

            @Override
            public void connectionLost(Throwable cause) {

            }

            @Override
            public void messageArrived(String topic, MqttMessage message) throws Exception {
                Log.w("Debug", message.toString());
                Log.w("Debug", topic);
                switch (topic) {
                    case subscriptionTopic:
                        dataTemp.setText(message.toString());
                        break;
                    case subscriptionTopic2:
                        dataLed.setText(message.toString());
                        break;
                    case subscriptionTopic3:
                        dataDoor.setText(message.toString());
                        break;
                }

            }

            @Override
            public void deliveryComplete(IMqttDeliveryToken token) {

            }



        });
    }


    @Override
    public void onClick(View v) {
        if(v.getId() == R.id.ledBtn){
            String viesti = "Click";
            MqttMessage message = new MqttMessage(viesti.getBytes());
            try {
                mqttHelper.mqttAndroidClient.publish("ledscontrol", message);
            } catch (MqttException exce){
                System.err.println("Exception whilst subscribing");
                exce.printStackTrace();
            }
        }

    }
}



