import xml.etree.ElementTree as ET
from .ebo_xml_builder import EBOXMLBuilder


class EBOModbusBuilder(EBOXMLBuilder):
    """
    A class to build Modbus Device, Modbus Register Group and Modbus Register objects as an XML structure for importing objects into EBO.
    This class extends the EBOXMLBuilder class and provides methods to create
    Modbus-related XML elements.

    Example XML structure:
    <OI NAME="Fire Gateway 1" TYPE="modbus.network.TCPDevice">
      <PI Name="IPAddress" Value="192.168.168.69"/>
      <OI NAME="Modbus Register Group Loop Devices" TYPE="modbus.point.ModbusRegisterGroup">
        <PI Name="GroupPollIntervalRequested" Value="13000"/>
        <OI DESCR="{{Description}}" NAME="L1 - D2 - Z5 - IRD-ICG-B04-SIC-05 COMMS CUPBOARD - OPT - ALARM" TYPE="modbus.point.BinaryInput">
          <PI Name="BitMask" Value="16"/>
          <PI Name="NOTE1" Value="{{Note1}}"/>
          <PI Name="NOTE2" Value="{{Note2}}"/>
          <PI Name="ReadFunctionCode" Value="3"/>
          <PI Name="RegisterNumber" Value="242"/>
          <PI Name="RegisterType" Value="1"/>
        </OI>
      </OI>
      <OI NAME="Modbus Register Group Loops" TYPE="modbus.point.ModbusRegisterGroup">
        <OI DESCR="{{Description}}" NAME="LOOP L2 - N1 - OPEN CIRCUIT" TYPE="modbus.point.BinaryInput">
          <PI Name="BitMask" Value="1"/>
          <PI Name="NOTE1" Value="{{Note1}}"/>
          <PI Name="NOTE2" Value="{{Note2}}"/>
          <PI Name="ReadFunctionCode" Value="3"/>
          <PI Name="RegisterNumber" Value="152"/>
          <PI Name="RegisterType" Value="1"/>
        </OI>
      </OI>
      <OI NAME="Some Digital Coil" TYPE="modbus.point.BinaryInput">
        <PI Name="RegisterNumber" Value="102"/>
      </OI>
    </OI>

    Example usage:
        builder = ModbusBuilder()
        device = builder.create_device(name="Fire Gateway 1", ip_address="192.168.168.69")
        group1 = builder.create_modbus_register_group(name="Modbus Register Group Loop Devices", poll_interval=13000)
        point1 = builder.create_holding_register_point(type="BinaryInput", register_type="16 bit unsigned" name="L1 - D2 - Z5 - IRD-ICG-B04-SIC-05 COMMS CUPBOARD - OPT - ALARM", register_number=242, bit_mask=16,  register_type=1, read_function_code=3, description="{{Description}}", note1="{{Note1}}", note2="{{Note2}}")
        group2 = builder.create_modbus_register_group(name="Modbus Register Group Loops")
        point2 = builder.create_point(type="BinaryInput", name="LOOP L2 - N1 - OPEN CIRCUIT", register_number=152, bit_mask=1, register_type=1, read_function_code=3, description="{{Description}}", note1="{{Note1}}", note2="{{Note2}}")
        builder.add_integer_value_pairs_to_event(event_1, tvp_values_event_1)
        builder.add_integer_value_pairs_to_event(event_2, tvp_values_event_2)
        schedule = builder.create_multistate_schedule("Office Light Schedule", schedule_default=0)
        builder.add_special_events_to_schedule(schedule, [event_1, event_2])
        builder.add_to_exported_objects(schedule)
    """

    def __init__(self, ebo_version="6.0.4.90", server_full_path="/Server 1"):
        super().__init__(ebo_version, server_full_path)

    @staticmethod
    def get_register_type_value(register_type_str):
        """
        Returns the corresponding register type number for a given register type string.
        Example:
            "Digital coil" -> None (leave out)
            "16 bit unsigned" -> 1
            "16 bit signed"   -> 2
            "32 bit unsigned" -> 3
            "32 bit signed"   -> 5
        """
        mapping = {
            "Digital coil": None,
            "16 bit unsigned": 1,
            "16 bit signed": 2,
            "32 bit unsigned": 3,
            "32 bit signed": 5,
        }
        if register_type_str not in mapping:
            raise ValueError(
                f"Invalid register type '{register_type_str}'. Must be one of: {', '.join(mapping.keys())}"
            )
        return mapping.get(register_type_str, None)

    @staticmethod
    def get_point_type_value(point_type_str):
        """
        Returns the corresponding Modbus point TYPE string for a given point type.
        Example:
            "BinaryInput"  -> "modbus.point.BinaryInput"
            "AnalogInput"  -> "modbus.point.AnalogInput"
            "IntegerInput" -> "modbus.point.IntegerInput"
        Raises ValueError if the type is not supported.
        """
        mapping = {
            "BinaryInput": "modbus.point.BinaryInput",
            "AnalogInput": "modbus.point.AnalogInput",
            "IntegerInput": "modbus.point.IntegerInput",
        }
        if point_type_str not in mapping:
            raise ValueError(
                f"Invalid point type '{point_type_str}'. Must be one of: {', '.join(mapping.keys())}"
            )
        return mapping[point_type_str]

    def create_device(self, name, ip_address=None, description=None):
        """
        Create a Modbus device XML element.

        :param name: The name of the device.
        :param ip_address: The IP address of the device (optional).
        :return: An XML element representing the Modbus device.
        """
        attribs = {
            "NAME": name,
            "TYPE": "modbus.network.TCPDevice",
        }
        if description is not None:
            attribs["DESCR"] = description

        device = ET.Element("OI", attribs)
        if ip_address:
            ET.SubElement(device, "PI", {"Name": "IPAddress", "Value": ip_address})
        return device

    def create_modbus_register_group(self, name, poll_interval=None):
        """
        Create a Modbus Register Group XML element.

        :param name: The name of the register group.
        :param poll_interval: The poll interval for the group (optional).
        :return: An XML element representing the Modbus Register Group.
        """
        group = ET.Element(
            "OI", {"NAME": name, "TYPE": "modbus.point.ModbusRegisterGroup"}
        )
        if poll_interval is not None:
            ET.SubElement(
                group,
                "PI",
                {
                    "Name": "GroupPollIntervalRequested",
                    "Value": str(int(poll_interval)),
                },
            )
        return group

    def create_point(
        self,
        name,
        register_number=101,
        bit_mask=None,
        type="BinaryInput",
        register_type=None,
        read_function_code=None,
        description=None,
        note1=None,
        note2=None,
    ):
        """
        Create a Modbus Point XML element. Only Read Only currently supported.

        :param name: The name of the point.
        :param type: The type of the point (default is "BinaryInput").
        :param register_type: The type of the register (optional, if undefined will default to "Digital coil" when imported).
        :param register_number: The register number, relative reference (ie 40001 is holding register 1) (default is 101).
        :param bit_mask: The bit mask for the point (optional).
        :param read_function_code: The read function code (optional, if undefined will default to 2 when imported).
        :param description: A description for the point (optional).
        :param note1: Note 1 for the point (optional).
        :param note2: Note 2 for the point (optional).
        :return: An XML element representing the Modbus Holding Register Point.
        """
        attribs = {
            "NAME": name,
            "TYPE": f"modbus.point.{type}",
        }
        if description is not None:
            attribs["DESCR"] = description

        point = ET.Element("OI", attribs)
        ET.SubElement(
            point,
            "PI",
            {
                "Name": "RegisterNumber",
                "Value": str(int(register_number)),
            },
        )
        if register_type is not None:
            if self.get_register_type_value(register_type) is not None:
                ET.SubElement(
                    point,
                    "PI",
                    {
                        "Name": "RegisterType",
                        "Value": str(self.get_register_type_value(register_type)),
                    },
                )
        if read_function_code is not None:
            ET.SubElement(
                point,
                "PI",
                {"Name": "ReadFunctionCode", "Value": str(int(read_function_code))},
            )

        if bit_mask is not None:
            ET.SubElement(point, "PI", {"Name": "BitMask", "Value": str(int(bit_mask))})

        if note1:
            ET.SubElement(point, "PI", {"Name": "NOTE1", "Value": note1})

        if note2:
            ET.SubElement(point, "PI", {"Name": "NOTE2", "Value": note2})

        return point

    def create_holding_register_point(
        self,
        name,
        register_number=1,
        bit_mask=None,
        type="BinaryInput",
        register_type="16 bit unsigned",
        read_function_code=3,
        description=None,
        note1=None,
        note2=None,
    ):
        """
        Create a Modbus Holding Register Point XML element. Only Read Only BinaryInput currently supported.

        :param name: The name of the point.
        :param type: The type of the point (default is "BinaryInput").
        :param register_type: The type of the register (default is "16 bit unsigned").
        :param register_number: The holding register number, relative reference (ie 40001 is 1) (default is 1).
        :param bit_mask: The bit mask for the point (optional).
        :param read_function_code: The read function code (default is 3).
        :param description: A description for the point (optional).
        :param note1: Note 1 for the point (optional).
        :param note2: Note 2 for the point (optional).
        :return: An XML element representing the Modbus Holding Register Point.
        """
        return self.create_point(
            name=name,
            register_number=register_number,
            bit_mask=bit_mask,
            type=type,
            register_type=register_type,
            read_function_code=read_function_code,
            description=description,
            note1=note1,
            note2=note2,
        )


if __name__ == "__main__":
    # Example usage
    builder = EBOModbusBuilder(ebo_version="5.0.3.117")
    device = builder.create_device(name="Fire Gateway 1", ip_address="192.168.168.69")
    group1 = builder.create_modbus_register_group(
        name="Modbus Register Group Loop Devices", poll_interval=13000
    )
    point1 = builder.create_holding_register_point(
        name="L1 - D2 - Z5 - IRD-ICG-B04-SIC-05 COMMS CUPBOARD - OPT - ALARM",
        register_number=242,
        bit_mask=16,
        description="{{Description}}",
        note1="{{Note1}}",
        note2="{{Note2}}",
    )
    group1.append(point1)
    group2 = builder.create_modbus_register_group(name="Modbus Register Group Loops")
    point2 = builder.create_holding_register_point(
        name="LOOP L2 - N1 - OPEN CIRCUIT",
        register_number=152,
        bit_mask=1,
        description="{{Description}}",
        note1="{{Note1}}",
        note2="{{Note2}}",
    )
    group2.append(point2)
    point3 = builder.create_point("Some Default Digital Coil")
    device.append(group1)
    device.append(group2)
    device.append(point3)
    builder.add_to_exported_objects(device)

    print(builder.to_pretty_xml())
    builder.write_xml("modbus.xml")
