import QtQuick 2.15
import QtQuick.Controls 2.15
import QtQuick.Layouts 1.15
import QtGraphicalEffects 1.15

Rectangle {
    id: root
    width: 520
    height: 420
    color: "transparent"

    // Signal definitions
    signal copyCodeClicked()
    signal retryClicked()
    signal closeClicked()

    Rectangle {
        id: mainContainer
        anchors.fill: parent
        anchors.margins: 8  // Space for shadow
        color: "#ffffff"
        radius: 10  // QML rounded corners, provides better anti-aliasing
        border.width: 0
        antialiasing: true

        // Add window shadow effect
        layer.enabled: true
        layer.effect: DropShadow {
            horizontalOffset: 0
            verticalOffset: 2
            radius: 10
            samples: 16
            color: "#15000000"
            transparentBorder: true
        }

        ColumnLayout {
            anchors.fill: parent
            anchors.margins: 20
            spacing: 20

            // ArcoDesign title area
            RowLayout {
                Layout.fillWidth: true
                spacing: 16

                Text {
                    text: "Device Activation"
                    font.family: "PingFang SC, Microsoft YaHei UI, Helvetica Neue"
                    font.pixelSize: 20
                    font.weight: Font.Medium
                    color: "#1d2129"
                }

                Item { Layout.fillWidth: true }

                // Activation status display area
                RowLayout {
                    spacing: 8

                    Rectangle {
                        width: 6
                        height: 6
                        radius: 3
                        color: activationModel ? getArcoStatusColor() : "#f53f3f"

                        function getArcoStatusColor() {
                            var status = activationModel.activationStatus
                            if (status === "Activated") return "#00b42a"
                            if (status === "Activating...") return "#ff7d00"
                            if (status.includes("mismatch")) return "#f53f3f"
                            return "#f53f3f"
                        }
                    }

                    Text {
                        text: activationModel ? activationModel.activationStatus : "Not Activated"
                        font.family: "PingFang SC, Microsoft YaHei UI"
                        font.pixelSize: 12
                        color: "#4e5969"
                    }
                }

                // Close button
                Button {
                    id: windowCloseBtn
                    width: 32
                    height: 32

                    background: Rectangle {
                        color: windowCloseBtn.pressed ? "#f53f3f" :
                               windowCloseBtn.hovered ? "#ff7875" : "transparent"
                        radius: 3
                        border.width: 0
                        antialiasing: true

                        // Color transition animation
                        Behavior on color {
                            ColorAnimation {
                                duration: 200
                                easing.type: Easing.OutCubic
                            }
                        }

                        // Scale animation
                        scale: windowCloseBtn.pressed ? 0.9 : (windowCloseBtn.hovered ? 1.1 : 1.0)
                        Behavior on scale {
                            NumberAnimation {
                                duration: 150
                                easing.type: Easing.OutCubic
                            }
                        }
                    }

                    contentItem: Text {
                        text: "×"
                        color: windowCloseBtn.hovered ? "white" : "#86909c"
                        font.family: "Arial"
                        font.pixelSize: 18
                        font.weight: Font.Bold
                        horizontalAlignment: Text.AlignHCenter
                        verticalAlignment: Text.AlignVCenter

                        // Text color transition animation
                        Behavior on color {
                            ColorAnimation {
                                duration: 200
                                easing.type: Easing.OutCubic
                            }
                        }
                    }

                    onClicked: root.closeClicked()
                }
            }

            // ArcoDesign device information card - compact display
            Rectangle {
                id: deviceInfoCard
                Layout.fillWidth: true
                Layout.preferredHeight: 80
                color: deviceInfoMouseArea.containsMouse ? "#f2f3f5" : "#f7f8fa"
                radius: 3
                border.width: 0
                antialiasing: true

                // Color transition animation
                Behavior on color {
                    ColorAnimation {
                        duration: 200
                        easing.type: Easing.OutCubic
                    }
                }

                // Mouse hover detection
                MouseArea {
                    id: deviceInfoMouseArea
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                }

                ColumnLayout {
                    anchors.fill: parent
                    anchors.leftMargin: 16
                    anchors.rightMargin: 16
                    spacing: 0

                    Item { Layout.fillHeight: true } // Top spacer

                    // Device information area
                    ColumnLayout {
                        Layout.fillWidth: true
                        spacing: 8

                        Text {
                            text: "Device Information"
                            font.family: "PingFang SC, Microsoft YaHei UI"
                            font.pixelSize: 13
                            font.weight: Font.Medium
                            color: "#4e5969"
                        }

                        GridLayout {
                            Layout.fillWidth: true
                            columns: 2
                            columnSpacing: 48
                            rowSpacing: 6

                            Text {
                                text: "Device Serial Number"
                                font.family: "PingFang SC, Microsoft YaHei UI"
                                font.pixelSize: 12
                                color: "#86909c"
                            }

                            Text {
                                text: "MAC Address"
                                font.family: "PingFang SC, Microsoft YaHei UI"
                                font.pixelSize: 12
                                color: "#86909c"
                            }

                            Text {
                                text: activationModel ? activationModel.serialNumber : "SN-7B46DAF2-00ff732a9678"
                                font.family: "SF Mono, Consolas, monospace"
                                font.pixelSize: 12
                                color: "#1d2129"
                            }

                            Text {
                                text: activationModel ? activationModel.macAddress : "00:ff:73:2a:96:78"
                                font.family: "SF Mono, Consolas, monospace"
                                font.pixelSize: 12
                                color: "#1d2129"
                            }
                        }
                    }

                    Item { Layout.fillHeight: true } // Bottom spacer
                }
            }

            // ArcoDesign activation code card - single line display
            Rectangle {
                id: activationCodeCard
                Layout.fillWidth: true
                Layout.preferredHeight: 64
                color: activationCodeMouseArea.containsMouse ? "#f2f3f5" : "#f7f8fa"
                radius: 3
                border.width: 0
                antialiasing: true

                // Color transition animation
                Behavior on color {
                    ColorAnimation {
                        duration: 200
                        easing.type: Easing.OutCubic
                    }
                }

                // Mouse hover detection
                MouseArea {
                    id: activationCodeMouseArea
                    anchors.fill: parent
                    hoverEnabled: true
                    cursorShape: Qt.PointingHandCursor
                }

                RowLayout {
                    anchors.fill: parent
                    anchors.leftMargin: 16
                    anchors.rightMargin: 16
                    spacing: 16

                    Text {
                        text: "Activation Code"
                        font.family: "PingFang SC, Microsoft YaHei UI"
                        font.pixelSize: 13
                        font.weight: Font.Medium
                        color: "#4e5969"
                    }

                    Rectangle {
                        Layout.fillWidth: true
                        height: 36
                        color: "#ffffff"
                        radius: 3
                        border.color: "#e5e6eb"
                        border.width: 1
                        antialiasing: true

                        Text {
                            anchors.centerIn: parent
                            text: activationModel ? activationModel.activationCode : "825523"
                            font.family: "SF Mono, Consolas, monospace"
                            font.pixelSize: 15
                            font.weight: Font.Medium
                            color: "#f53f3f"
                            font.letterSpacing: 2
                        }
                    }

                    Button {
                        id: copyCodeBtn
                        text: "Copy"
                        Layout.preferredWidth: 80
                        height: 36

                        background: Rectangle {
                            color: copyCodeBtn.pressed ? "#0e42d2" :
                                   copyCodeBtn.hovered ? "#4080ff" : "#165dff"
                            radius: 3
                            border.width: 0
                            antialiasing: true

                            // Color transition animation
                            Behavior on color {
                                ColorAnimation {
                                    duration: 200
                                    easing.type: Easing.OutCubic
                                }
                            }

                            // Scale animation
                            scale: copyCodeBtn.pressed ? 0.95 : (copyCodeBtn.hovered ? 1.05 : 1.0)
                            Behavior on scale {
                                NumberAnimation {
                                    duration: 150
                                    easing.type: Easing.OutCubic
                                }
                            }
                        }

                        font.family: "PingFang SC, Microsoft YaHei UI"
                        font.pixelSize: 13
                        palette.buttonText: "white"

                        onClicked: root.copyCodeClicked()
                    }
                }
            }

            // ArcoDesign button area
            RowLayout {
                Layout.fillWidth: true
                Layout.preferredHeight: 40
                spacing: 16

                Button {
                    id: retryBtn
                    text: "Go to Activation"
                    Layout.fillWidth: true
                    Layout.preferredHeight: 36

                    background: Rectangle {
                        color: retryBtn.pressed ? "#0e42d2" :
                               retryBtn.hovered ? "#4080ff" : "#165dff"
                        radius: 3
                        border.width: 0
                        antialiasing: true

                        // Color transition animation
                        Behavior on color {
                            ColorAnimation {
                                duration: 200
                                easing.type: Easing.OutCubic
                            }
                        }

                        // Scale animation
                        scale: retryBtn.pressed ? 0.98 : (retryBtn.hovered ? 1.02 : 1.0)
                        Behavior on scale {
                            NumberAnimation {
                                duration: 150
                                easing.type: Easing.OutCubic
                            }
                        }

                        // Add subtle shadow
                        layer.enabled: true
                        layer.effect: DropShadow {
                            horizontalOffset: 0
                            verticalOffset: 2
                            radius: 6
                            samples: 12
                            color: "#20165dff"
                        }
                    }

                    font.family: "PingFang SC, Microsoft YaHei UI"
                    font.pixelSize: 14
                    font.weight: Font.Medium
                    palette.buttonText: "white"

                    onClicked: root.retryClicked()
                }
            }
        }
    }
}
