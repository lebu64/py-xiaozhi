import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtGraphicalEffects 1.15

Rectangle {
    id: root
    width: 800
    height: 500
    color: "#f5f5f5"

    // Signal definitions - connect with Python callbacks
    signal manualButtonPressed()
    signal manualButtonReleased()
    signal autoButtonClicked()
    signal abortButtonClicked()
    signal modeButtonClicked()
    signal sendButtonClicked(string text)
    signal settingsButtonClicked()
    // Title bar related signals
    signal titleMinimize()
    signal titleClose()
    signal titleDragStart(real mouseX, real mouseY)
    signal titleDragMoveTo(real mouseX, real mouseY)
    signal titleDragEnd()

    // Main layout
    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 0
        spacing: 0

        // Custom title bar: minimize, close, draggable
        Rectangle {
            id: titleBar
            Layout.fillWidth: true
            Layout.preferredHeight: 36
            color: "#f7f8fa"
            border.width: 0

            // Whole title bar drag (using screen coordinates to avoid cumulative error causing jitter)
            // Placed at the bottom layer so button MouseArea can respond first
            MouseArea {
                anchors.fill: parent
                acceptedButtons: Qt.LeftButton
                onPressed: {
                    root.titleDragStart(mouse.x, mouse.y)
                }
                onPositionChanged: {
                    if (pressed) {
                        root.titleDragMoveTo(mouse.x, mouse.y)
                    }
                }
                onReleased: {
                    root.titleDragEnd()
                }
                z: 0  // Bottom layer
            }

            RowLayout {
                anchors.fill: parent
                anchors.leftMargin: 10
                anchors.rightMargin: 8
                spacing: 8
                z: 1  // Button layer above drag layer

                // Left drag area
                Item { id: dragArea; Layout.fillWidth: true; Layout.fillHeight: true }

                // Minimize
                Rectangle {
                    id: btnMin
                    width: 24; height: 24; radius: 6
                    color: btnMinMouse.pressed ? "#e5e6eb" : (btnMinMouse.containsMouse ? "#f2f3f5" : "transparent")
                    z: 2  // Ensure button is at the top layer
                    Text { anchors.centerIn: parent; text: "–"; font.pixelSize: 14; color: "#4e5969" }
                    MouseArea {
                        id: btnMinMouse
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: root.titleMinimize()
                    }
                }

                // Close
                Rectangle {
                    id: btnClose
                    width: 24; height: 24; radius: 6
                    color: btnCloseMouse.pressed ? "#f53f3f" : (btnCloseMouse.containsMouse ? "#ff7875" : "transparent")
                    z: 2  // Ensure button is at the top layer
                    Text { anchors.centerIn: parent; text: "×"; font.pixelSize: 14; color: btnCloseMouse.containsMouse ? "white" : "#86909c" }
                    MouseArea {
                        id: btnCloseMouse
                        anchors.fill: parent
                        hoverEnabled: true
                        onClicked: root.titleClose()
                    }
                }
            }
        }

        // Status card area
        Rectangle {
            id: statusCard
            Layout.fillWidth: true
            Layout.fillHeight: true
            color: "transparent"

            ColumnLayout {
                anchors.fill: parent
                anchors.margins: 20
                spacing: 20

                // Status label
                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 48
                    color: "#E3F2FD"
                    radius: 12

                    Text {
                        anchors.centerIn: parent
                        text: displayModel ? displayModel.statusText : "Status: Not connected"
                        font.family: "PingFang SC, Microsoft YaHei UI"
                        font.pixelSize: 14
                        font.weight: Font.Bold
                        color: "#2196F3"
                    }
                }

                // Emotion display area
                Item {
                    Layout.fillWidth: true
                    Layout.fillHeight: true
                    Layout.minimumHeight: 120

                    // Dynamic emotion loading: AnimatedImage for GIF, Image for static images, Text for emoji
                    Loader {
                        id: emotionLoader
                        anchors.centerIn: parent
                        width: Math.min(parent.width * 0.8, 200)
                        height: Math.min(parent.height * 0.8, 200)

                        sourceComponent: {
                            var path = displayModel ? displayModel.emotionPath : ""
                            if (!path || path.length === 0) {
                                return emojiComponent
                            }
                            if (path.indexOf(".gif") !== -1) {
                                return gifComponent
                            }
                            if (path.indexOf(".") !== -1) {
                                return imageComponent
                            }
                            return emojiComponent
                        }

                        // GIF animation component
                        Component {
                            id: gifComponent
                            AnimatedImage {
                                fillMode: Image.PreserveAspectFit
                                source: displayModel ? ("file://" + displayModel.emotionPath) : ""
                                playing: true
                                speed: 1.05
                                cache: true
                            }
                        }

                        // Static image component
                        Component {
                            id: imageComponent
                            Image {
                                fillMode: Image.PreserveAspectFit
                                source: displayModel ? ("file://" + displayModel.emotionPath) : ""
                                cache: true
                            }
                        }

                        // Emoji text component
                        Component {
                            id: emojiComponent
                            Text {
                                text: displayModel ? displayModel.emotionPath : "😊"
                                font.pixelSize: 80
                                horizontalAlignment: Text.AlignHCenter
                                verticalAlignment: Text.AlignVCenter
                            }
                        }
                    }
                }

                // TTS text display area
                Rectangle {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 80
                    color: "transparent"

                    Text {
                        anchors.fill: parent
                        anchors.margins: 15
                        text: displayModel ? displayModel.ttsText : "Standby"
                        font.family: "PingFang SC, Microsoft YaHei UI"
                        font.pixelSize: 14
                        color: "#555555"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                        wrapMode: Text.WordWrap
                    }
                }
            }
        }

        // Button area (unified colors and dimensions)
        Rectangle {
            Layout.fillWidth: true
            Layout.preferredHeight: 72
            color: "#f7f8fa"

            RowLayout {
                anchors.fill: parent
                anchors.leftMargin: 16
                anchors.rightMargin: 16
                anchors.bottomMargin: 12
                spacing: 10

                // Manual mode button (hold to speak) - primary color
                Button {
                    id: manualBtn
                    Layout.preferredWidth: 140
                    Layout.preferredHeight: 40
                    text: "Hold to speak"
                    visible: displayModel ? !displayModel.autoMode : true

                    background: Rectangle {
                        color: manualBtn.pressed ? "#0e42d2" : (manualBtn.hovered ? "#4080ff" : "#165dff")
                        radius: 8

                        Behavior on color { ColorAnimation { duration: 120; easing.type: Easing.OutCubic } }
                    }

                    contentItem: Text {
                        text: manualBtn.text
                        font.family: "PingFang SC, Microsoft YaHei UI"
                        font.pixelSize: 13
                        color: "white"
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter
                    }

                    onPressed: { manualBtn.text = "Release to stop"; root.manualButtonPressed() }
                    onReleased: { manualBtn.text = "Hold to speak"; root.manualButtonReleased() }
                }

                // Auto mode button - primary color
                Button {
                    id: autoBtn
                    Layout.preferredWidth: 140
                    Layout.preferredHeight: 40
                    text: displayModel ? displayModel.buttonText : "Start conversation"
                    visible: displayModel ? displayModel.autoMode : false

                    background: Rectangle {
                        color: autoBtn.pressed ? "#0e42d2" : (autoBtn.hovered ? "#4080ff" : "#165dff")
                        radius: 8
                        Behavior on color { ColorAnimation { duration: 120; easing.type: Easing.OutCubic } }
                    }

                    contentItem: Text { text: autoBtn.text; font.family: "PingFang SC, Microsoft YaHei UI"; font.pixelSize: 13; color: "white"; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                    onClicked: root.autoButtonClicked()
                }

                // Interrupt conversation - secondary color
                Button {
                    id: abortBtn
                    Layout.preferredWidth: 120
                    Layout.preferredHeight: 40
                    text: "Interrupt"

                    background: Rectangle { color: abortBtn.pressed ? "#e5e6eb" : (abortBtn.hovered ? "#f2f3f5" : "#eceff3"); radius: 8 }
                    contentItem: Text { text: abortBtn.text; font.family: "PingFang SC, Microsoft YaHei UI"; font.pixelSize: 13; color: "#1d2129"; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                    onClicked: root.abortButtonClicked()
                }

                // Input + Send
                RowLayout {
                    Layout.fillWidth: true
                    Layout.preferredHeight: 40
                    spacing: 8

                    Rectangle {
                        Layout.fillWidth: true
                        Layout.preferredHeight: 40
                        color: "white"
                        radius: 8
                        border.color: textInput.activeFocus ? "#165dff" : "#e5e6eb"
                        border.width: 1

                        TextInput {
                            id: textInput
                            anchors.fill: parent
                            anchors.leftMargin: 12
                            anchors.rightMargin: 12
                            verticalAlignment: TextInput.AlignVCenter
                            font.family: "PingFang SC, Microsoft YaHei UI"
                            font.pixelSize: 13
                            color: "#333333"
                            selectByMouse: true
                            clip: true

                            // Placeholder
                            Text { anchors.fill: parent; text: "Enter text..."; font: textInput.font; color: "#c9cdd4"; verticalAlignment: Text.AlignVCenter; visible: !textInput.text && !textInput.activeFocus }

                            Keys.onReturnPressed: { if (textInput.text.trim().length > 0) { root.sendButtonClicked(textInput.text); textInput.text = "" } }
                        }
                    }

                    Button {
                        id: sendBtn
                        Layout.preferredWidth: 84
                        Layout.preferredHeight: 40
                        text: "Send"
                        background: Rectangle { color: sendBtn.pressed ? "#0e42d2" : (sendBtn.hovered ? "#4080ff" : "#165dff"); radius: 8 }
                        contentItem: Text { text: sendBtn.text; font.family: "PingFang SC, Microsoft YaHei UI"; font.pixelSize: 13; color: "white"; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                        onClicked: { if (textInput.text.trim().length > 0) { root.sendButtonClicked(textInput.text); textInput.text = "" } }
                    }
                }

                // Mode (secondary)
                Button {
                    id: modeBtn
                    Layout.preferredWidth: 120
                    Layout.preferredHeight: 40
                    text: displayModel ? displayModel.modeText : "Manual conversation"
                    background: Rectangle { color: modeBtn.pressed ? "#e5e6eb" : (modeBtn.hovered ? "#f2f3f5" : "#eceff3"); radius: 8 }
                    contentItem: Text { text: modeBtn.text; font.family: "PingFang SC, Microsoft YaHei UI"; font.pixelSize: 13; color: "#1d2129"; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                    onClicked: root.modeButtonClicked()
                }

                // Settings (secondary)
                Button {
                    id: settingsBtn
                    Layout.preferredWidth: 120
                    Layout.preferredHeight: 40
                    text: "Settings"
                    background: Rectangle { color: settingsBtn.pressed ? "#e5e6eb" : (settingsBtn.hovered ? "#f2f3f5" : "#eceff3"); radius: 8 }
                    contentItem: Text { text: settingsBtn.text; font.family: "PingFang SC, Microsoft YaHei UI"; font.pixelSize: 13; color: "#1d2129"; horizontalAlignment: Text.AlignHCenter; verticalAlignment: Text.AlignVCenter }
                    onClicked: root.settingsButtonClicked()
                }
            }
        }
    }
}
