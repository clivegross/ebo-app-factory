from ebo_app_factory.schedule_builder import EBOScheduleBuilder


def test_create_schedule_and_events():
    builder = EBOScheduleBuilder(ebo_version="5.0.3.117")
    # Create TVP values for two events
    tvp_values_event_1 = [
        {"Hour": 6, "Minute": 13, "Value": 1},
        {"Hour": 16, "Minute": 30, "Value": 9},
    ]
    tvp_values_event_2 = [
        {"Hour": 7, "Minute": 0, "Value": 2},
        {"Hour": 18, "Minute": 15, "Value": 3},
    ]

    # Create two special events
    event_1 = builder.create_schedule_special_event(
        event_name="05-01", day_of_month=1, month=5
    )
    event_2 = builder.create_schedule_special_event(
        event_name="05-02", day_of_month=2, month=5
    )

    # Add TVP pairs to events
    builder.add_integer_value_pairs_to_event(event_1, tvp_values_event_1)
    builder.add_integer_value_pairs_to_event(event_2, tvp_values_event_2)

    # Create schedule and add events
    schedule = builder.create_multistate_schedule("Test Schedule", schedule_default=0)
    builder.add_special_events_to_schedule(schedule, [event_1, event_2])

    # Add to exported objects and get XML
    builder.add_to_exported_objects(schedule)
    xml_str = builder.to_pretty_xml()
    print(xml_str)

    # Basic checks
    assert '<SourceVersion Value="5.0.3.117"/>' in xml_str
    assert '<OI NAME="Test Schedule" TYPE="schedule.NSPMultistateSchedule">' in xml_str
    assert '<PI Name="ScheduleDefault" Value="0"/>' in xml_str
    assert '<PI Name="EventName" Value="05-01"/>' in xml_str
    assert '<PI Name="EventName" Value="05-02"/>' in xml_str
    assert '<PI Name="Hour" Value="6"/>' in xml_str
    assert '<PI Name="Minute" Value="13"/>' in xml_str
    assert '<PI Name="Value" Value="1"/>' in xml_str
