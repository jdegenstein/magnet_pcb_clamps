# %%
from build123d import *
from ocp_vscode import *

set_port(3939)
show_clear()
set_defaults(ortho=True, default_edgecolor="#121212", reset_camera=Camera.KEEP)
# %%


######## Create the base part

base_od = 10 * 2
base_id = 6.05 * 2
base_h = 8
base_fillet_rad = 2
base_cbore_h = 3
base_bolt_id = 2.1 * 2
base_hex_flats = 7.664
base_hex_h = 3

with BuildPart() as p_base:
    with BuildSketch() as s_base_outer:
        Circle(base_od / 2)
    extrude(amount=base_h)
    fillet(faces().sort_by(Axis.Z)[-1].edges(), base_fillet_rad)
    with BuildSketch() as s_base_inner:
        Circle(base_id / 2)
    extrude(amount=base_cbore_h, mode=Mode.SUBTRACT)
    with BuildSketch(Plane.XY.offset(base_cbore_h)) as s_base_hex:
        RegularPolygon(base_hex_flats / 2, 6, major_radius=False, rotation=30)
    extrude(amount=base_hex_h, mode=Mode.SUBTRACT)
    Hole(base_bolt_id / 2)

######## Create the floating clamp part

floating_clamp_od = 7.5 * 2
floating_clamp_len = 30
floating_clamp_wid = 6.220
floating_clamp_round = 2
floating_clamp_h = 3
floating_clamp_minor_od = 5 * 2
floating_clamp_minor_h = 3
floating_clamp_id = 2.1 * 2

with BuildPart() as p_floating_clamp:
    with BuildSketch() as s_fc_base:
        RectangleRounded(floating_clamp_len, floating_clamp_wid, floating_clamp_round)
        Circle(floating_clamp_od / 2)
    extrude(amount=floating_clamp_h)
    with BuildSketch(Plane.XY.offset(floating_clamp_h)) as s_fc_top:
        Circle(floating_clamp_minor_od / 2)
    extrude(amount=floating_clamp_minor_h)
    Hole(floating_clamp_id / 2)

######## Create the top clamp part

top_clamp_od = 7.5 * 2
top_clamp_h = 4
top_clamp_fillet = 2
top_clamp_cbore_d1 = 2 * 2
top_clamp_cbore_d2 = 3.5 * 2
top_clamp_cbore_h = 2

with BuildPart() as p_top_clamp:
    with BuildSketch() as s_tc:
        Circle(top_clamp_od / 2)
    extrude(amount=top_clamp_h)
    fillet(faces().sort_by(Axis.Z)[-1].edges(), top_clamp_fillet)
    with Locations(Plane.XY.offset(top_clamp_h)):
        CounterBoreHole(
            top_clamp_cbore_d1 / 2, top_clamp_cbore_d2 / 2, top_clamp_cbore_h
        )

######## display statements

set_colormap(ColorMap.seeded(colormap="rgb", alpha=1, seed_value="vscod"))
# fmt: off
show_all(
    classes = [BuildPart, BuildSketch, BuildLine, ],  # comment to show all objects
    include = ["base_step", "floating_clamp", "top_clamp"],
    exclude = ["", ],
    show_sketch_local = False,
    helper_scale = 1,  # controls size of e.g. planes and axes
)  # fmt: on


# %%
######## export statements for STL and STEP:

export_stl(p_base.part, "base.stl")
export_stl(p_floating_clamp.part, "floating_clamp.stl")
export_stl(p_top_clamp.part, "top_clamp.stl")

export_step(p_base.part, "base.step")
export_step(p_floating_clamp.part, "floating_clamp.step")
export_step(p_top_clamp.part, "top_clamp.step")
