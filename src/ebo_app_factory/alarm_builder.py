import xml.etree.ElementTree as ET
from .ebo_xml_builder import EBOXMLBuilder


class EBOAlarmBuilder(EBOXMLBuilder):
    """
    A class to build Alarm XML objects for EBO import.
    """

    def __init__(self, ebo_version="6.0.4.90", server_full_path="/Server 1"):
        super().__init__(ebo_version, server_full_path)

    def create_change_of_state_alarm(
        self,
        name,
        description=None,
        note1=None,
        note2=None,
        alarm_message=None,
        reset_message=None,
        category=None,
        monitored_variable=None,
        priority=None,
        attachment=None,
        **kwargs,
    ):
        """
        Create a ChangeOfStateAlarm XML element.

        :param name: The name of the alarm (required).
        :param description: Optional description for the alarm.
        :param note1: Optional NOTE1.
        :param note2: Optional NOTE2.
        :param alarm_message: Optional alarm message.
        :param reset_message: Optional reset message.
        :param category: Optional category reference path.
        :param monitored_variable: Optional monitored variable reference path.
        :param priority: Optional alarm priority (int or str).
        :param attachment: Optional attachment object reference.
        :param kwargs: Additional parameters (not used in this method).
        :return: An XML element representing the ChangeOfStateAlarm.
        """
        attribs = {
            "NAME": name,
            "TYPE": "alarm.ChangeOfStateAlarm",
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
        if monitored_variable is not None:
            mon_pi = ET.SubElement(alarm, "PI", {"Name": "MonitoredVariable"})
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
        if note1 is not None:
            ET.SubElement(alarm, "PI", {"Name": "NOTE1", "Value": note1})
        if note2 is not None:
            ET.SubElement(alarm, "PI", {"Name": "NOTE2", "Value": note2})
        if reset_message is not None:
            ET.SubElement(alarm, "PI", {"Name": "ResetMessage", "Value": reset_message})
        # TODO: add support for TimeDelayToNormal
        # ET.SubElement(alarm, "PI", {"Name": "TimeDelayToNormal", "Value": "2"})

        # Example: Add an Attachment child (optional, can be parameterized)
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
