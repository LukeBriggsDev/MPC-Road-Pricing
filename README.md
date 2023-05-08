# MPC Road Pricing
This is the implementation for a simulation of an electronic road pricing scheme which uses Multi-Party Computation.

# Requirements
- [MP-SPDZ](https://github.com/data61/MP-SPDZ)
- [Requests](https://pypi.org/project/requests/)
- [IO-VNBD](https://github.com/onyekpeu/IO-VNBD)

## Animate.py
- [Matplotlib](https://pypi.org/project/matplotlib/)
- [Numpy](https://pypi.org/project/numpy/)
- [PyProj](https://pypi.org/project/pyproj/)

## Compiling MPC

- Compile and install MP-SPDZ for your platform under the `mpspdz` directory. 
- mpc.py should be in your mp-spdz installation directory under `Programs/Source`
- Run `./compile_mpc.sh`.
  - You may need to edit the compile script depending on which arithmetic domain your protocol requires.

## Running MPC
A single run of the MPC can be completed using the example inputs in `mpspdz/Player-Data`

## Running Simulation
- Have the IO-VNBD dataset in the same directory as the `mpspdz` folder
- Start `mpc_service.py`
- In another terminal run `agent.py`
- MPC output will be recorded in `data-export` in the format `<lat> <long> <price> <distance>`
