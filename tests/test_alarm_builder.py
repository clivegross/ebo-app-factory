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


# Recreate this Sum Alarm object
# <OI NAME="Sum Alarm" TYPE="alarm.SumAlarm">
#   <PI Name="AutoHide" Value="1"/>
#   <PI Name="Category">
#     <Reference DeltaFilter="0" Locked="1" Object="~/System/Alarm Control Panel/Alarm Handling/Categories/Fire" Retransmit="0" TransferRate="10"/>
#   </PI>
#         <PI Name="AlarmMessage" Value="@(SourceObject-&gt;NOTE1) - @(SourceObject-&gt;DESCR)"/>
#         <PI Name="ResetMessage" Value="@(SourceObject-&gt;NOTE1) - @(SourceObject-&gt;DESCR) Returned to Normal"/>
#         <PI Name="AlarmPriority" Value="1"/>
#         <PI Name="ResetPriority" Value="1"/>
#         <PI Name="NOTE1" Value="Fire Detection Zone Z1"/>
#         <PI Name="NOTE2" Value="IRD-ICG-B05"/>
#   <OI NAME="Filter" TYPE="event.filter.Filter" declared="1" hidden="1">
#     <OI NAME="Source" TYPE="event.filter.expression.Text" flags="aggregated" hidden="1">
#       <PI Name="Column" Value="Source"/>
#       <PI Name="DisplayName" Value="Source"/>
#       <OI NAME="Value1" TYPE="event.filter.expression.TextValue" flags="aggregated" hidden="1">
#         <PI Name="Value" Value="* Z1 *- ALARM"/>
#       </OI>
#     </OI>
#     <OI NAME="Category" TYPE="event.filter.expression.Text" flags="aggregated" hidden="1">
#       <PI Name="Column" Value="Category"/>
#       <PI Name="DisplayName" Value="Category"/>
#       <OI NAME="Value1" TYPE="event.filter.expression.TextValue" flags="aggregated" hidden="1">
#         <PI Name="Value" Value="Fire"/>
#       </OI>
#     </OI>
#     <OI NAME="AlarmState" TYPE="event.filter.expression.Enum" flags="aggregated" hidden="1">
#       <PI Name="Column" Value="AlarmState"/>
#       <PI Name="DisplayName" Value="Alarm state"/>
#       <PI Name="EnumType" Value="alarm.pt.AlarmState"/>
#       <OI NAME="1" TYPE="event.filter.expression.EnumValue" flags="aggregated" hidden="1">
#         <PI Name="Value" Value="1"/>
#       </OI>
#       <OI NAME="2" TYPE="event.filter.expression.EnumValue" flags="aggregated" hidden="1">
#         <PI Name="Value" Value="2"/>
#       </OI>
#     </OI>
#   </OI>
# </OI>
def test_create_sum_alarm(tmp_path):
    builder = EBOAlarmBuilder(ebo_version="5.0.3.117")
    alarm = builder.create_sum_alarm(
        name="Sum Alarm",
        alarm_message="@(SourceObject->NOTE1) - @(SourceObject->DESCR)",
        reset_message="@(SourceObject->NOTE1) - @(SourceObject->DESCR) Returned to Normal",
        priority=1,
        category="~/System/Alarm Control Panel/Alarm Handling/Categories/Fire",
        note1="Fire Detection Zone Z1",
        note2="IRD-ICG-B05",
        attachment="../../../../../_Common/Graphics/ICG-B05 Fire",
        conditions_values={
            "Source": ["* Z1 *- ALARM"],
            "Category": ["Fire"],
            "AlarmState": [1, 2],
        },
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
    assert '<OI NAME="Sum Alarm" TYPE="alarm.SumAlarm">' in xml_from_file
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
    # check filter
    assert (
        '<OI NAME="Filter" TYPE="event.filter.Filter" declared="1" hidden="1">'
        in xml_from_file
    )
    # Source filter
    assert (
        '<OI NAME="Source" TYPE="event.filter.expression.Text" flags="aggregated" hidden="1">'
        in xml_from_file
    )
    assert '<PI Name="Column" Value="Source"/>' in xml_from_file
    assert '<PI Name="DisplayName" Value="Source"/>' in xml_from_file
    assert (
        '<OI NAME="Value1" TYPE="event.filter.expression.TextValue" flags="aggregated" hidden="1">'
        in xml_from_file
    )
    assert '<PI Name="Value" Value="* Z1 *- ALARM"/>' in xml_from_file
    # Category filter
    assert (
        '<OI NAME="Category" TYPE="event.filter.expression.Text" flags="aggregated" hidden="1">'
        in xml_from_file
    )
    assert '<PI Name="Column" Value="Category"/>' in xml_from_file
    assert '<PI Name="DisplayName" Value="Category"/>' in xml_from_file
    assert (
        '<OI NAME="Value1" TYPE="event.filter.expression.TextValue" flags="aggregated" hidden="1">'
        in xml_from_file
    )
    assert '<PI Name="Value" Value="Fire"/>' in xml_from_file
    # AlarmState filter
    assert (
        '<OI NAME="AlarmState" TYPE="event.filter.expression.Enum" flags="aggregated" hidden="1">'
        in xml_from_file
    )
    assert '<PI Name="Column" Value="AlarmState"/>' in xml_from_file
    assert '<PI Name="DisplayName" Value="Alarm state"/>' in xml_from_file
    assert '<PI Name="EnumType" Value="alarm.pt.AlarmState"/>' in xml_from_file
    assert (
        '<OI NAME="1" TYPE="event.filter.expression.EnumValue" flags="aggregated" hidden="1">'
        in xml_from_file
    )
    assert '<PI Name="Value" Value="1"/>' in xml_from_file
    assert (
        '<OI NAME="2" TYPE="event.filter.expression.EnumValue" flags="aggregated" hidden="1">'
        in xml_from_file
    )
    assert '<PI Name="Value" Value="2"/>' in xml_from_file


# Recreate this Alarm View object:
# <OI NAME="Alarm View" TYPE="alarm.AlarmViewer">
#   <OI NAME="Filter" TYPE="event.filter.Filter" declared="1" hidden="1">
#     <OI NAME="Category" TYPE="event.filter.expression.Text" flags="aggregated" hidden="1">
#       <PI Name="Column" Value="Category"/>
#       <PI Name="DisplayName" Value="Category"/>
#       <PI Name="Operator" Value="0"/>
#       <OI NAME="Value1" TYPE="event.filter.expression.TextValue" flags="aggregated" hidden="1">
#         <PI Name="Value" Value="Fire"/>
#       </OI>
#     </OI>
#     <OI NAME="Source" TYPE="event.filter.expression.Text" flags="aggregated" hidden="1">
#       <PI Name="Column" Value="Source"/>
#       <PI Name="DisplayName" Value="Source"/>
#       <PI Name="Operator" Value="0"/>
#       <OI NAME="Value1" TYPE="event.filter.expression.TextValue" flags="aggregated" hidden="1">
#         <PI Name="Value" Value="* Z1 *- ALARM"/>
#       </OI>
#       <OI NAME="Value2" TYPE="event.filter.expression.TextValue" flags="aggregated" hidden="1">
#         <PI Name="Value" Value="*Sum Alarm*"/>
#       </OI>
#     </OI>
#   </OI>
# </OI>
def test_create_alarm_view(tmp_path):
    builder = EBOAlarmBuilder(ebo_version="5.0.3.117")

    alarm_view = builder.create_alarm_view(
        name="My Alarm View",
        description="Test Alarm Viewer",
        note1="This is a test NOTE1",
        note2="This is a test NOTE2",
        conditions_values={
            "Category": ["Fire"],
            "Source": ["* Z1 *- ALARM", "*Sum Alarm*"],
        },
    )

    builder.add_to_exported_objects(alarm_view)
    xml_str = builder.to_pretty_xml()
    print(xml_str)

    output_path = os.path.join(tmp_path, "alarm_view.xml")
    builder.write_xml(output_path)

    assert os.path.exists(output_path), "Output XML file not created"

    with open(output_path, "r", encoding="utf-8") as f:
        xml = f.read()

    # Header and object
    assert '<SourceVersion Value="5.0.3.117"/>' in xml
    assert '<OI NAME="My Alarm View" TYPE="alarm.AlarmViewer"' in xml
    assert 'DESCR="Test Alarm Viewer"' in xml

    # NOTE1 and NOTE2
    assert '<PI Name="NOTE1" Value="This is a test NOTE1"/>' in xml
    assert '<PI Name="NOTE2" Value="This is a test NOTE2"/>' in xml

    # Filter root
    assert (
        '<OI NAME="Filter" TYPE="event.filter.Filter" declared="1" hidden="1">' in xml
    )

    # Category filter block
    assert (
        '<OI NAME="Category" TYPE="event.filter.expression.Text" flags="aggregated" hidden="1">'
        in xml
    )
    assert '<PI Name="Column" Value="Category"/>' in xml
    assert '<PI Name="DisplayName" Value="Category"/>' in xml
    assert '<PI Name="Value" Value="Fire"/>' in xml

    # Source filter block
    assert (
        '<OI NAME="Source" TYPE="event.filter.expression.Text" flags="aggregated" hidden="1">'
        in xml
    )
    assert '<PI Name="Column" Value="Source"/>' in xml
    assert '<PI Name="DisplayName" Value="Source"/>' in xml
    # TODO: is this operator prop required?
    # assert '<PI Name="Operator" Value="0"/>' in xml
    assert '<PI Name="Value" Value="* Z1 *- ALARM"/>' in xml
    assert '<PI Name="Value" Value="*Sum Alarm*"/>' in xml
