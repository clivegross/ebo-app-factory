from ebo_app_factory.modbus_builder import EBOModbusBuilder


def test_create_device_and_point():
    builder = EBOModbusBuilder(ebo_version="5.0.3.117")
    device = builder.create_device(name="Test Device", ip_address="192.168.1.100")
    group = builder.create_modbus_register_group(name="Test Group", poll_interval=10000)
    point = builder.create_holding_register_point(
        name="Test Point",
        register_number=123,
        bit_mask=8,
        description="Test Description",
        note1="Note1",
        note2="Note2",
    )
    group.append(point)
    device.append(group)
    default_point = builder.create_point(name="Default Digital Coil")
    device.append(default_point)
    builder.add_to_exported_objects(device)
    xml_str = builder.to_pretty_xml()
    print(xml_str)
    # Basic checks
    assert '<SourceVersion Value="5.0.3.117"/>' in xml_str
    assert '<OI NAME="Test Device" TYPE="modbus.network.TCPDevice">' in xml_str
    assert '<PI Name="GroupPollIntervalRequested" Value="10000"/>' in xml_str
    assert '<PI Name="IPAddress" Value="192.168.1.100"/>' in xml_str
    assert '<OI NAME="Test Group" TYPE="modbus.point.ModbusRegisterGroup">' in xml_str
    assert '<PI Name="RegisterNumber" Value="123"/>' in xml_str
    assert '<OI NAME="Default Digital Coil" TYPE="modbus.point.BinaryInput">' in xml_str
