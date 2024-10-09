import streamlit as st

def recalculate(resistance, current):
    voltage = current * resistance
    power = current * voltage
    power = power / 1000
    return power, voltage
#definitions
kA_turns = 30 #kA-turns
mag_field = 1 #Tesla
TMS_zdim = 7.0 #meter
copper_area = 0.0016 #meters^2
copper_resistivity = 0.0000000168 #Ohm*meter
temp_coefficient = 0.00404 #Kelvin^(-1)
temp_0 = 20 #celcius
corner_plates = 120
corner_interconnects = 600
coil_current = 1200 #amp

# Title of the UI
st.title("Coil and Power Spec Calculator (Current == 1200amps/turn)")
# Sidebar for parameter input
st.sidebar.header("Adjust Parameters")
# User inputs
TMS_width = st.sidebar.slider("TMS x-dimension (width) (meters)", min_value=5.0, max_value=7.0, step=1.0, value=7.0)
PS_connector_length = st.sidebar.slider("Length of power supply interconnects (pos/neg)(meter)", min_value=1.0, max_value=15.0, step=1.0, value=4.0)
PS_connector_efficiency = st.sidebar.slider("Interconnect resistivity compared to copper bars (%)", min_value=10.0, max_value=1000.0, step=10.0, value=100.0) / 100
corner_plate_resistance = st.sidebar.slider("Average resistance of corner plate (microohms)", min_value=10, max_value=1000, step=10, value=100) / 1000000
corner_length = st.sidebar.slider("Length of longest corner interconnect (cm)", min_value=1.0, max_value=40.0, step=1.0, value=25.0) / 100
#if power > 1000/power_supplies:
#    power_supplies >= coil_breakdown
#current_limit = st.sidebar.slider("Power Supply Current Limit (A)", min_value=10.0, max_value=2000.0, step=10.0, value=1000.0)
#coil_breakdown = st.sidebar.slider("Number of coil sections", min_value=1.0, max_value=6.0, step=1.0, value=1.0)
coil_temp = st.sidebar.slider("Expected temperature of coil", min_value=20.0, max_value=500.0, step=10.0, value=50.0)
corner_resistance = corner_length * copper_resistivity * corner_interconnects / (copper_area * 0.35) #corner_length divided by 2 and 0.7 cross-sectional area
corner = st.checkbox('Is corner connector a plate[Y] or stranded interconnect[N]', value=False)
if corner:
    corner_resistance = corner_plates * corner_plate_resistance 

#coil totals
coil_length = 300*TMS_zdim + 100*TMS_width
temp_dependent_resistivity = copper_resistivity*(1 + temp_coefficient*(coil_temp - temp_0))
coil_resistance = temp_dependent_resistivity * coil_length / copper_area
PS_connector_resistance = temp_dependent_resistivity * PS_connector_length * PS_connector_efficiency / copper_area
total_resistance = coil_resistance + PS_connector_resistance + corner_resistance

# Button to recalculate
if st.sidebar.button("Recalculate"):
    # Perform the recalculation
    power, voltage = recalculate(total_resistance, coil_current)
    
    # Display the results
    st.write(f"**Calculated Power:** {power:.2f} kWatt")
    st.write(f"**Calculated Voltage:** {voltage:.2f} V")
    #st.line_chart(chart_data)

# Instructions for the user
st.write("Use the sliders in the sidebar to adjust the parameters, and click the 'Recalculate' button.")
