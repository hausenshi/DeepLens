"""
"Hello, world!" for DeepLens.
 
In this code, we will load a lens from a file. Then we will plot the lens setup and render a sample image.
 
Technical Paper:
    [1] Xinge Yang, Qiang Fu and Wolfgang Heidrich, "Curriculum learning for ab initio deep learned refractive optics," Nature Communications 2024.
    [2] Congli Wang, Ni Chen, and Wolfgang Heidrich, "dO: A differentiable engine for Deep Lens design of computational imaging systems," IEEE TCI 2023.
 
This code and data is released under the Creative Commons Attribution-NonCommercial 4.0 International license (CC BY-NC.) In a nutshell:
    # The license is only for non-commercial use (commercial licenses can be obtained from authors).
    # The material is provided as-is, with no warranties whatsoever.
    # If you publish any code, data, or scientific work based on this, please cite our work.
"""
 
from deeplens import GeoLens
 
 
def init_constraints(lens: GeoLens):
    """Initialize constraints for the lens design. Unit [mm]."""
    lens.is_cellphone = False
 
    # Self intersection constraints
    lens.dist_min = 0.0
    lens.dist_max = float("inf")
    lens.thickness_min = 1.0
    lens.thickness_max = 100.0
    lens.flange_min = 0.5
    lens.flange_max = float("inf")
 
    # Surface curvature constraints
    lens.sag_max = 30.0
    lens.grad_max = 5.0
    lens.grad2_max = 100.0
    lens.d_to_t_max = 10.0
    lens.tmax_to_tmin_max = 5.0
 
    # Chief ray angle constraints
    lens.chief_ray_angle_max = 20.0
 
 
def main():
    # Initialize lens
    lens = GeoLens(filename='./results/0704-101-DesignLens/iter1000.json')
    init_constraints(lens)
 
    # Lens optimization
    lens.optimize(
        lrs=[1e-4, 1e-4, 1e-3, 1e-4],
        decay=0.001,
        iterations=10000,
        test_per_iter=100,
        centroid=False,
        optim_mat=True,
        # match_mat=False, 
        shape_control=True,
        # sample_more_off_axis=True,
    )
 
    # Evaluate lens
    lens.analysis(render=False)
 
    # lens.write_lens_zmx()
    # lens.write_lens_json()
 
if __name__ == "__main__":
    main()