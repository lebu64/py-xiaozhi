import paho.mqtt.client as mqtt


class MqttClient:
    def __init__(
        self,
        server,
        port,
        username,
        password,
        subscribe_topic,
        publish_topic=None,
        client_id="PythonClient",
        on_connect=None,
        on_message=None,
        on_publish=None,
        on_disconnect=None,
    ):
        """Initialize MqttClient instance.

        :param server: MQTT server address
        :param port: MQTT server port
        :param username: Login username
        :param password: Login password
        :param subscribe_topic: Subscription topic
        :param publish_topic: Publish topic
        :param client_id: Client ID, defaults to "PythonClient"
        :param on_connect: Custom connection callback function
        :param on_message: Custom message receive callback function
        :param on_publish: Custom message publish callback function
        :param on_disconnect: Custom disconnect callback function
        """
        self.server = server
        self.port = port
        self.username = username
        self.password = password
        self.subscribe_topic = subscribe_topic
        self.publish_topic = publish_topic
        self.client_id = client_id

        # Create MQTT client instance using the latest API version
        self.client = mqtt.Client(client_id=self.client_id, protocol=mqtt.MQTTv5)

        # Set username and password
        self.client.username_pw_set(self.username, self.password)

        # Set callback functions, use custom ones if provided, otherwise use defaults
        if on_connect:
            self.client.on_connect = on_connect
        else:
            self.client.on_connect = self._on_connect

        self.client.on_message = on_message if on_message else self._on_message
        self.client.on_publish = on_publish if on_publish else self._on_publish

        if on_disconnect:
            self.client.on_disconnect = on_disconnect
        else:
            self.client.on_disconnect = self._on_disconnect

    def _on_connect(self, client, userdata, flags, rc, properties=None):
        """
        Default connection callback function.
        """
        if rc == 0:
            print("✅ Successfully connected to MQTT server")
            # Automatically subscribe to topic after successful connection
            client.subscribe(self.subscribe_topic)
            print(f"📥 Subscribed to topic: {self.subscribe_topic}")
        else:
            print(f"❌ Connection failed, error code: {rc}")

    def _on_message(self, client, userdata, msg):
        """
        Default message receive callback function.
        """
        topic = msg.topic
        content = msg.payload.decode()
        print(f"📩 Received message - Topic: {topic}, Content: {content}")

    def _on_publish(self, client, userdata, mid, properties=None):
        """
        Default message publish callback function.
        """
        print(f"📤 Message published, message ID: {mid}")

    def _on_disconnect(self, client, userdata, rc, properties=None):
        """
        Default disconnect callback function.
        """
        print("🔌 Disconnected from MQTT server")

    def connect(self):
        """
        Connect to MQTT server.
        """
        try:
            self.client.connect(self.server, self.port, 60)
            print(f"🔗 Connecting to server {self.server}:{self.port}")
        except Exception as e:
            print(f"❌ Connection failed, error: {e}")

    def start(self):
        """
        Start client and begin network loop.
        """
        self.client.loop_start()

    def publish(self, message):
        """
        Publish message to specified topic.
        """
        result = self.client.publish(self.publish_topic, message)
        status = result.rc
        if status == 0:
            print(f"✅ Successfully published to topic `{self.publish_topic}`")
        else:
            print(f"❌ Publish failed, error code: {status}")

    def stop(self):
        """
        Stop network loop and disconnect.
        """
        self.client.loop_stop()
        self.client.disconnect()
        print("🛑 Client connection stopped")


if __name__ == "__main__":
    pass
    # Custom callback functions
    # def custom_on_connect(client, userdata, flags, rc, properties=None):
    #     if rc == 0:
    #         print("🎉 Custom callback: Successfully connected to MQTT server")
    #         topic_data = userdata['subscribe_topic']
    #         client.subscribe(topic_data)
    #         print(f"📥 Custom callback: Subscribed to topic: {topic_data}")
    #     else:
    #         print(f"❌ Custom callback: Connection failed, error code: {rc}")
    #
    # def custom_on_message(client, userdata, msg):
    #     topic = msg.topic
    #     content = msg.payload.decode()
    #     print(f"📩 Custom callback: Received message - Topic: {topic}, Content: {content}")
    #
    # def custom_on_publish(client, userdata, mid, properties=None):
    #     print(f"📤 Custom callback: Message published, message ID: {mid}")
    #
    # def custom_on_disconnect(client, userdata, rc, properties=None):
    #     print("🔌 Custom callback: Disconnected from MQTT server")
    #
    # # Create MqttClient instance, pass custom callback functions
    # mqtt_client = MqttClient(
    #     server="8.130.181.98",
    #     port=1883,
    #     username="admin",
    #     password="dtwin@123",
    #     subscribe_topic="sensors/temperature/request",
    #     publish_topic="sensors/temperature/device_001/state",
    #     client_id="CustomClient",
    #     on_connect=custom_on_connect,
    #     on_message=custom_on_message,
    #     on_publish=custom_on_publish,
    #     on_disconnect=custom_on_disconnect
    # )
    #
    # # Pass subscription topic information as user data to callback functions
    # mqtt_client.client.user_data_set(
    #     {'subscribe_topic': mqtt_client.subscribe_topic}
    # )
    #
    # # Connect to MQTT server
    # mqtt_client.connect()
    #
    # # Start client
    # mqtt_client.start()
    #
    # try:
    #     while True:
    #         # Publish message
    #         message = input("Enter message to publish: ")
    #         mqtt_client.publish(message)
    # except KeyboardInterrupt:
    #     print("\n⛔️ Program stopped")
    # finally:
    #     # Stop and disconnect
    #     mqtt_client.stop()
