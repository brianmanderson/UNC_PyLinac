from PlotScrollNumpyArrays import plot_scroll_Image
from pylinac.winston_lutz import WinstonLutz, MachineScale, Axis
import os


def get_last_number(filename):
    # Get the base name in case you have a full path
    base = os.path.basename(filename)
    # Remove the extension (assuming '.dcm' is 4 characters)
    if base.lower().endswith('.dcm'):
        base = base[:-4]
    # Split by '.' and convert the last part to an integer
    return int(base.split('.')[-1])


def main():
    # TODO Change path to files! you can use r'\\radoncphysics\DATA\RIT_QA_Images\UNC\FOLDER'
    path_to_files = os.path.join('.', 'Data')
    files = [i for i in os.listdir(path_to_files) if i.endswith('.dcm')]
    sorted_files = sorted(files, key=get_last_number)
    """
    Mapping values refer to gantry, collimator, couch
    """
    gantry_collimator_couch_angles = [
        (180, 270, 0),
        (180, 90, 0),
        (270, 90, 0),
        (270, 270, 0),
        (0, 270, 0),
        (0, 90, 0),
        (90, 90, 0),
        (90, 270, 0)
    ]
    bb_size_mm = 7
    mapping = {filename: angle for filename, angle in zip(sorted_files, gantry_collimator_couch_angles)}
    print('File name                                     Gantry Collimator Couch')
    for key in mapping.keys():
        print(f"{key} mapped to {mapping[key]}")
    wl = WinstonLutz(directory=path_to_files, axis_mapping=mapping)
    wl.analyze(bb_size_mm=bb_size_mm, machine_scale=MachineScale.ELEKTA_IEC, low_density_bb=False)
    print(wl.bb_shift_instructions())
    wl.plot_images()
    wl.publish_pdf(os.path.join(path_to_files, 'Results.pdf'))


if __name__ == '__main__':
    main()
