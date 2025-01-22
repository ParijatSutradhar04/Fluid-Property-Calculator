import streamlit as st
from pyfluids import Fluid, FluidsList, Phases, Input


# Streamlit app
def main():
    st.title("Fluid State Calculator")

    # Fluid selection
    st.subheader("Select a Fluid")
    fluid_names = [f.name for f in FluidsList]
    fluid_name = st.selectbox("Choose a fluid", fluid_names)
    fluid = Fluid(getattr(FluidsList, fluid_name))

    # Parameter inputs
    st.subheader("Input Parameters")
    param_options = ["pressure", "temperature", "enthalpy", "entropy", "density"]
    param1_name = st.selectbox("First parameter", param_options)
    param1_value = st.number_input(f"Enter value for {param1_name} (SI units)", value=0.0, step=1.0)

    param2_name = st.selectbox("Second parameter", [p for p in param_options if p != param1_name])
    param2_value = st.number_input(f"Enter value for {param2_name} (SI units, temp in C)", value=0.0, step=1.0)

    # Calculate fluid state
    if st.button("Calculate"):
        param_map = {
            "pressure": Input.pressure,
            "temperature": Input.temperature,
            "enthalpy": Input.enthalpy,
            "entropy": Input.entropy,
            "density": Input.density,
        }

        try:
            fluid = fluid.with_state(param_map[param1_name](param1_value), param_map[param2_name](param2_value))

            # Handle two-phase region
            if fluid.phase == Phases.TwoPhase:
                st.warning("The fluid is in a two-phase region. Vapor quality (x) is required.")
                vapor_quality = st.number_input("Enter vapor quality (x) (between 0 and 1)", min_value=0.0, max_value=1.0, value=0.5, step=0.01)
                fluid = fluid.with_state(param_map[param1_name](param1_value), Input.quality(vapor_quality))

            # Display results
            st.subheader("Fluid Properties")
            fluid_properties = fluid.as_dict()
            for key, value in fluid_properties.items():
                st.write(f"{key}: {value}")

        except ValueError as e:
            st.error(f"Error: {e}")


if __name__ == "__main__":
    main()