import xml.etree.ElementTree as ET
from .ebo_xml_builder import EBOXMLBuilder


class EBOAlarmBuilder(EBOXMLBuilder):
    """
    A class to build Alarm XML objects for EBO import.
    """

    CHANGE_OF_STATE_ALARM_TYPE = "alarm.ChangeOfStateAlarm"
    SUM_ALARM_TYPE = "alarm.SumAlarm"
    EVENT_FILTER_TYPE = "event.filter.Filter"
    ALARM_VIEWER_TYPE = "alarm.AlarmViewer"

    def __init__(self, ebo_version="6.0.4.90", server_full_path="/Server 1"):
        super().__init__(ebo_version, server_full_path)

    def _create_alarm_oi(
        self,
        name,
        alarm_type,
        description=None,
        note1=None,
        note2=None,
        alarm_message=None,
        reset_message=None,
        category=None,
        priority=None,
        attachment=None,
        extra_pis=None,
    ):
        attribs = {
            "NAME": name,
            "TYPE": alarm_type,
        }
        if description is not None:
            attribs["DESCR"] = description

        alarm = ET.Element("OI", attribs)

        if alarm_message is not None:
            ET.SubElement(alarm, "PI", {"Name": "AlarmMessage", "Value": alarm_message})
        if priority is not None:
            ET.SubElement(
                alarm, "PI", {"Name": "AlarmPriority", "Value": str(priority)}
            )
            ET.SubElement(
                alarm, "PI", {"Name": "ResetPriority", "Value": str(priority)}
            )
        if category is not None:
            cat_pi = ET.SubElement(alarm, "PI", {"Name": "Category"})
            ET.SubElement(
                cat_pi,
                "Reference",
                {
                    "DeltaFilter": "0",
                    "Locked": "1",
                    "Object": category,
                    "Retransmit": "0",
                    "TransferRate": "10",
                },
            )
        if note1 is not None:
            ET.SubElement(alarm, "PI", {"Name": "NOTE1", "Value": note1})
        if note2 is not None:
            ET.SubElement(alarm, "PI", {"Name": "NOTE2", "Value": note2})
        if reset_message is not None:
            ET.SubElement(alarm, "PI", {"Name": "ResetMessage", "Value": reset_message})

        # Add any extra PI elements (as a list of dicts)
        if extra_pis:
            for pi in extra_pis:
                ET.SubElement(alarm, "PI", pi)

        # Attachment
        if attachment is not None:
            attachment_oi = ET.SubElement(
                alarm,
                "OI",
                {
                    "NAME": "Attachment",
                    "TYPE": "alarm.attachments.Attachment",
                    "flags": "aggregated",
                    "hidden": "1",
                },
            )
            obj_ref_pi = ET.SubElement(attachment_oi, "PI", {"Name": "ObjectReference"})
            ET.SubElement(
                obj_ref_pi,
                "Reference",
                {
                    "DeltaFilter": "0",
                    "Object": attachment,
                    "Retransmit": "0",
                    "TransferRate": "10",
                },
            )

        return alarm

    def _set_monitored_variable(self, obj, monitored_variable):
        """
        Example monitored variable XML object:
        <PI Name="MonitoredVariable">
            <Reference DeltaFilter="0" Object="../../../../../../../../Interfaces/Modbus TCP Network/Fire Detection System/Ampac FFP Gateway 1/zones_Z1_to_Z1000/Zone Z1 - TOWER 2 BASEMENT 5 - ALARM" Property="Value" Retransmit="0" TransferRate="10"/>
        </PI>
        """
        mon_pi = ET.SubElement(obj, "PI", {"Name": "MonitoredVariable"})
        ET.SubElement(
            mon_pi,
            "Reference",
            {
                "DeltaFilter": "0",
                "Object": monitored_variable,
                "Property": "Value",
                "Retransmit": "0",
                "TransferRate": "10",
            },
        )
        return obj

    def _create_event_filter_condition_oi(self, condition, values, **kwargs):
        """
        Create an Event Filter Condition XML object.

        Args:
            - condition: Name of the filter condition (e.g., "Source", "Category", "AlarmState").
            - values: List of values for the condition. Note AlarmState values (1 = Alarm, 2 = Acknowledged)

        Returns:
            An XML Element representing the Event Filter Condition.

        Example:
        self._create_event_filter_condition_oi(condition="Source", values=["* Z1 *- ALARM"])

        returns:
        <OI NAME="Source" TYPE="event.filter.expression.Text" flags="aggregated" hidden="1">
          <PI Name="Column" Value="Source"/>
          <PI Name="DisplayName" Value="Source"/>
          <OI NAME="Value1" TYPE="event.filter.expression.TextValue" flags="aggregated" hidden="1">
            <PI Name="Value" Value="* Z1 *- ALARM"/>
          </OI>
        </OI>

        self._create_event_filter_condition_oi(condition="AlarmState", values=[1, 2])

        returns:
            <OI NAME="AlarmState" TYPE="event.filter.expression.Enum" flags="aggregated" hidden="1">
            <PI Name="Column" Value="AlarmState"/>
            <PI Name="DisplayName" Value="Alarm state"/>
            <PI Name="EnumType" Value="alarm.pt.AlarmState"/>
            <OI NAME="1" TYPE="event.filter.expression.EnumValue" flags="aggregated" hidden="1">
                <PI Name="Value" Value="1"/>
            </OI>
            <OI NAME="2" TYPE="event.filter.expression.EnumValue" flags="aggregated" hidden="1">
                <PI Name="Value" Value="2"/>
            </OI>
            </OI>
        """
        supported_conditions = {
            "Source": {
                "type": "event.filter.expression.Text",
                "value_type": "event.filter.expression.TextValue",
            },
            "Category": {
                "type": "event.filter.expression.Text",
                "value_type": "event.filter.expression.TextValue",
            },
            "AlarmState": {
                "type": "event.filter.expression.Enum",
                "EnumType": "alarm.pt.AlarmState",
                "value_type": "event.filter.expression.EnumValue",
            },
        }
        if condition not in supported_conditions:
            raise ValueError(f"Unsupported filter condition: {condition}")

        condition_meta = supported_conditions[condition]
        oi_attribs = {
            "NAME": condition,
            "TYPE": condition_meta["type"],
            "flags": "aggregated",
            "hidden": "1",
        }
        oi = ET.Element("OI", oi_attribs)
        ET.SubElement(oi, "PI", {"Name": "Column", "Value": condition})
        ET.SubElement(
            oi,
            "PI",
            {
                "Name": "DisplayName",
                "Value": condition if condition != "AlarmState" else "Alarm state",
            },
        )
        if "EnumType" in condition_meta:
            ET.SubElement(
                oi, "PI", {"Name": "EnumType", "Value": condition_meta["EnumType"]}
            )

        for idx, value in enumerate(values, start=1):
            if condition_meta["value_type"] == "event.filter.expression.EnumValue":
                oi_name = f"{idx}"
            else:
                oi_name = f"Value{idx}"
            value_oi_attribs = {
                "NAME": oi_name,
                "TYPE": condition_meta["value_type"],
                "flags": "aggregated",
                "hidden": "1",
            }
            value_oi = ET.SubElement(oi, "OI", value_oi_attribs)
            ET.SubElement(value_oi, "PI", {"Name": "Value", "Value": str(value)})

        return oi

    def _create_event_filter(self, conditions_values):
        """
        Create and return an Event Filter OI element (does NOT attach to parent).

        Args:
            - conditions_values: Dict mapping condition names to lists of values.
                Example: {"Source": ["* Z1 *- ALARM"], "Category": ["Fire"], "AlarmState": [1, 2]}

        Returns:
            The created filter OI element. eg
            <OI NAME="Filter" TYPE="event.filter.Filter" declared="1" hidden="1">
                ...conditions
            </OI>
        """
        filter_oi = ET.Element(
            "OI",
            {
                "NAME": "Filter",
                "TYPE": "event.filter.Filter",
                "declared": "1",
                "hidden": "1",
            },
        )
        for condition, values in conditions_values.items():
            cond_oi = self._create_event_filter_condition_oi(condition, values)
            filter_oi.append(cond_oi)
        return filter_oi

    def create_sum_alarm(self, name, conditions_values, **kwargs):
        """
        Create a Sum Alarm XML object.

        Args:
            name (str): The name of the sum alarm.
            conditions_values (dict): Dictionary mapping filter condition names to lists of values.
                Example: {"Source": ["* Z1 *- ALARM"], "Category": ["Fire"], "AlarmState": [1, 2]}
            **kwargs: Additional common alarm parameters (description, note1, note2, alarm_message, reset_message, category, priority, attachment, extra_pis).

        Returns:
            xml.etree.ElementTree.Element: The root OI element for the sum alarm.

        Example XML structure:
        <OI NAME="Sum Alarm" TYPE="alarm.SumAlarm">
            <PI Name="AutoHide" Value="1"/>
            <PI Name="Category">
                <Reference DeltaFilter="0" Locked="1" Object="~/System/Alarm Control Panel/Alarm Handling/Categories/Fire" Retransmit="0" TransferRate="10"/>
            </PI>
            <OI NAME="Filter" TYPE="event.filter.Filter" declared="1" hidden="1">
                <OI NAME="Source" TYPE="event.filter.expression.Text" flags="aggregated" hidden="1">
                    <PI Name="Column" Value="Source"/>
                    <PI Name="DisplayName" Value="Source"/>
                    <OI NAME="Value1" TYPE="event.filter.expression.TextValue" flags="aggregated" hidden="1">
                        <PI Name="Value" Value="* Z1 *- ALARM"/>
                    </OI>
                </OI>
                <OI NAME="Category" TYPE="event.filter.expression.Text" flags="aggregated" hidden="1">
                    <PI Name="Column" Value="Category"/>
                    <PI Name="DisplayName" Value="Category"/>
                    <OI NAME="Value1" TYPE="event.filter.expression.TextValue" flags="aggregated" hidden="1">
                        <PI Name="Value" Value="Fire"/>
                    </OI>
                </OI>
                <OI NAME="AlarmState" TYPE="event.filter.expression.Enum" flags="aggregated" hidden="1">
                    <PI Name="Column" Value="AlarmState"/>
                    <PI Name="DisplayName" Value="Alarm state"/>
                    <PI Name="EnumType" Value="alarm.pt.AlarmState"/>
                    <OI NAME="1" TYPE="event.filter.expression.EnumValue" flags="aggregated" hidden="1">
                        <PI Name="Value" Value="1"/>
                    </OI>
                    <OI NAME="2" TYPE="event.filter.expression.EnumValue" flags="aggregated" hidden="1">
                        <PI Name="Value" Value="2"/>
                    </OI>
                </OI>
            </OI>
        </OI>
        """
        if not conditions_values:
            print(
                "Warning: No filters provided for Sum Alarm. Sum Alarm will capture everything."
            )
        alarm = self._create_alarm_oi(
            name=name, alarm_type=self.SUM_ALARM_TYPE, **kwargs
        )
        # Add unique filter structure
        filter_oi = self._create_event_filter(conditions_values)
        alarm.append(filter_oi)
        return alarm

    def create_change_of_state_alarm(
        self,
        name,
        monitored_variable=None,  # unique/required for this alarm type
        **kwargs,  # all other common/optional params
    ):
        """
        Create a Change of State Alarm XML object.

        Args:
            - name:
            - monitored_variable:

        Example XML structure:
        <OI DESCR="Fire alarm in zone" NAME="Zone Z1 - ALARM" TYPE="alarm.ChangeOfStateAlarm">
            <PI Name="AlarmMessage" Value="@(SourceObject-&gt;NOTE1) - @(SourceObject-&gt;DESCR)"/>
            <PI Name="AlarmPriority" Value="1"/>
            <PI Name="Category">
            <Reference DeltaFilter="0" Locked="1" Object="~/System/Alarm Control Panel/Alarm Handling/Categories/Fire" Retransmit="0" TransferRate="10"/>
            </PI>
            <PI Name="MonitoredVariable">
            <Reference DeltaFilter="0" Object="../../../../../../../../Interfaces/Modbus TCP Network/Fire Detection System/Ampac FFP Gateway 1/zones_Z1_to_Z1000/Zone Z1 - TOWER 2 BASEMENT 5 - ALARM" Property="Value" Retransmit="0" TransferRate="10"/>
            </PI>
            <PI Name="NOTE1" Value="Zone Z1 - ICG-B05"/>
            <PI Name="NOTE2" Value="IRD-ICG-B05"/>
            <PI Name="ResetMessage" Value="@(SourceObject-&gt;NOTE1) - @(SourceObject-&gt;DESCR) Returned to Normal"/>
            <PI Name="ResetPriority" Value="1"/>
            <OI NAME="Attachment" TYPE="alarm.attachments.Attachment" flags="aggregated" hidden="1">
            <PI Name="ObjectReference">
                <Reference DeltaFilter="0" Object="../../../../../_Common/Graphics/ICG-B05 Fire" Retransmit="0" TransferRate="10"/>
            </PI>
            </OI>
            <OI NAME="Attachment_2" TYPE="alarm.attachments.Attachment" flags="aggregated" hidden="1">
            <PI Name="ObjectReference">
                <Reference DeltaFilter="0" Object="../../../../../../../_Common/Graphics/ICG-B05 Fire" Retransmit="0" TransferRate="10"/>
            </PI>
            </OI>
        </OI>
        """
        alarm = self._create_alarm_oi(
            name=name,
            alarm_type=self.CHANGE_OF_STATE_ALARM_TYPE,
            **kwargs,
        )
        if monitored_variable:
            self._set_monitored_variable(alarm, monitored_variable)
        return alarm

    def create_alarm_view(
        self,
        name="Alarm View",
        conditions_values=None,
        description=None,
        note1=None,
        note2=None,
    ):
        """
        Create Alarm View XML object.

        Example:
        <OI NAME="Alarm View" TYPE="alarm.AlarmViewer">
        <OI NAME="Filter" TYPE="event.filter.Filter" declared="1" hidden="1">
            <OI NAME="Category" TYPE="event.filter.expression.Text" flags="aggregated" hidden="1">
            <PI Name="Column" Value="Category"/>
            <PI Name="DisplayName" Value="Category"/>
            <PI Name="Operator" Value="0"/>
            <OI NAME="Value1" TYPE="event.filter.expression.TextValue" flags="aggregated" hidden="1">
                <PI Name="Value" Value="Fire"/>
            </OI>
            </OI>
            <OI NAME="Source" TYPE="event.filter.expression.Text" flags="aggregated" hidden="1">
            <PI Name="Column" Value="Source"/>
            <PI Name="DisplayName" Value="Source"/>
            <PI Name="Operator" Value="0"/>
            <OI NAME="Value1" TYPE="event.filter.expression.TextValue" flags="aggregated" hidden="1">
                <PI Name="Value" Value="* Z1 *- ALARM"/>
            </OI>
            <OI NAME="Value2" TYPE="event.filter.expression.TextValue" flags="aggregated" hidden="1">
                <PI Name="Value" Value="*Sum Alarm*"/>
            </OI>
            </OI>
        </OI>
        </OI>
        """
        attribs = {
            "NAME": name,
            "TYPE": self.ALARM_VIEWER_TYPE,
        }
        if description is not None:
            attribs["DESCR"] = description

        view = ET.Element("OI", attribs)
        if note1 is not None:
            ET.SubElement(view, "PI", {"Name": "NOTE1", "Value": note1})
        if note2 is not None:
            ET.SubElement(view, "PI", {"Name": "NOTE2", "Value": note2})
        # Add unique filter structure
        filter_oi = self._create_event_filter(conditions_values)
        view.append(filter_oi)
        return view
