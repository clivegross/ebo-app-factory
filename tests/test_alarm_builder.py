import os
from ebo_app_factory.alarm_builder import EBOAlarmBuilder

# Attempting to create a ChangeOfStateAlarm object similar to the one in the original code snippet
# <OI DESCR="Alarm" NAME="ZONE Z1 - ICG-B05 - ALARM" TYPE="alarm.ChangeOfStateAlarm">
#         <PI Name="AlarmMessage" Value="@(SourceObject-&gt;NOTE1) - @(SourceObject-&gt;DESCR)"/>
#         <PI Name="AlarmPriority" Value="1"/>
#         <PI Name="Category">
#           <Reference DeltaFilter="0" Locked="1" Object="~/System/Alarm Control Panel/Alarm Handling/Categories/Fire" Retransmit="0" TransferRate="10"/>
#         </PI>
#         <PI Name="MonitoredVariable">
#           <Reference DeltaFilter="0" Object="../../../../../../Interfaces/Modbus TCP Network/Fire Detection System/Ampac ICG-L02 Main Fire Alarm Control Panel Modbus TCP Gateway 1/6002-6251 Zone Status/Z1 ALARM" Property="Value" Retransmit="0" TransferRate="10"/>
#         </PI>
#         <PI Name="NOTE1" Value="Fire Detection Zone Z1"/>
#         <PI Name="NOTE2" Value="IRD-ICG-B05"/>
#         <PI Name="ResetMessage" Value="@(SourceObject-&gt;NOTE1) - @(SourceObject-&gt;DESCR) Returned to Normal"/>
#         <PI Name="ResetPriority" Value="1"/>
#         <PI Name="TimeDelayToNormal" Value="2"/>
#         <OI NAME="Attachment" TYPE="alarm.attachments.Attachment" flags="aggregated" hidden="1">
#           <PI Name="ObjectReference">
#             <Reference DeltaFilter="0" Object="../../../../../_Common/Graphics/ICG-B05 Fire" Retransmit="0" TransferRate="10"/>
#           </PI>
#         </OI>
#       </OI>


def test_create_change_of_state_alarm(tmp_path):
    builder = EBOAlarmBuilder(ebo_version="5.0.3.117")
    alarm = builder.create_change_of_state_alarm(
        name="ZONE Z1 - ICG-B05 - ALARM",
        alarm_message="@(SourceObject->NOTE1) - @(SourceObject->DESCR)",
        reset_message="@(SourceObject->NOTE1) - @(SourceObject->DESCR) Returned to Normal",
        priority=1,
        category="~/System/Alarm Control Panel/Alarm Handling/Categories/Fire",
        monitored_variable="../../../../../../Interfaces/Modbus TCP Network/Fire Detection System/Ampac ICG-L02 Main Fire Alarm Control Panel Modbus TCP Gateway 1/6002-6251 Zone Status/Z1 ALARM",
        note1="Fire Detection Zone Z1",
        note2="IRD-ICG-B05",
        attachment="../../../../../_Common/Graphics/ICG-B05 Fire",
    )
    builder.add_to_exported_objects(alarm)
    xml_str = builder.to_pretty_xml()
    print(xml_str)
    # Write to file
    output_path = os.path.join(tmp_path, "tmp_output.xml")
    builder.write_xml(output_path)
    assert os.path.exists(output_path), f"Output file {output_path} does not exist"
    with open(output_path, "r", encoding="utf-8") as f:
        xml_from_file = f.read()
    # Basic checks
    assert '<SourceVersion Value="5.0.3.117"/>' in xml_from_file
    assert (
        '<OI NAME="ZONE Z1 - ICG-B05 - ALARM" TYPE="alarm.ChangeOfStateAlarm">'
        in xml_from_file
    )
    assert (
        '<PI Name="AlarmMessage" Value="@(SourceObject-&gt;NOTE1) - @(SourceObject-&gt;DESCR)"/>'
        in xml_from_file
    )
    assert '<PI Name="AlarmPriority" Value="1"/>' in xml_from_file
    assert '<PI Name="Category">' in xml_from_file
    assert (
        '<Reference DeltaFilter="0" Locked="1" Object="~/System/Alarm Control Panel/Alarm Handling/Categories/Fire" Retransmit="0" TransferRate="10"/>'
        in xml_from_file
    )
    assert '<PI Name="MonitoredVariable">' in xml_from_file
    assert (
        '<Reference DeltaFilter="0" Object="../../../../../../Interfaces/Modbus TCP Network/Fire Detection System/Ampac ICG-L02 Main Fire Alarm Control Panel Modbus TCP Gateway 1/6002-6251 Zone Status/Z1 ALARM" Property="Value" Retransmit="0" TransferRate="10"/>'
        in xml_from_file
    )
    assert '<PI Name="NOTE1" Value="Fire Detection Zone Z1"/>' in xml_from_file
    assert '<PI Name="NOTE2" Value="IRD-ICG-B05"/>' in xml_from_file
    assert (
        '<PI Name="ResetMessage" Value="@(SourceObject-&gt;NOTE1) - @(SourceObject-&gt;DESCR) Returned to Normal"/>'
        in xml_from_file
    )
    assert '<PI Name="ResetPriority" Value="1"/>' in xml_from_file
    assert (
        '<OI NAME="Attachment" TYPE="alarm.attachments.Attachment" flags="aggregated" hidden="1">'
        in xml_from_file
    )
    assert '<PI Name="ObjectReference">' in xml_from_file
    assert (
        '<Reference DeltaFilter="0" Object="../../../../../_Common/Graphics/ICG-B05 Fire" Retransmit="0" TransferRate="10"/>'
        in xml_from_file
    )
