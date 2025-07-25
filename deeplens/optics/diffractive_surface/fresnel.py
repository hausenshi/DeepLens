"""Fresnel DOE. Phase fresnel lens has an inverse dispersion property compared to refractive lens.

Reference:
    [1] https://www.nikonusa.com/learn-and-explore/c/ideas-and-inspiration/phase-fresnel-from-wildlife-photography-to-portraiture
"""

import torch
from deeplens.optics.diffractive_surface.diffractive import DiffractiveSurface


class Fresnel(DiffractiveSurface):
    def __init__(
        self,
        d,
        f0=None,
        wvln0=0.55,
        res=(2000, 2000),
        mat="fused_silica",
        fab_ps=0.001,
        device="cpu",
    ):
        """Initialize Fresnel DOE. A diffractive Fresnel lens shows inverse dispersion property compared to refractive lens.

        Args:
            f0 (float): Initial focal length. [mm]
            d (float): Distance of the DOE surface. [mm]
            res (tuple or int): Resolution of the DOE, [w, h]. [pixel]
            wvln0 (float): Design wavelength. [um]
            mat (str): Material of the DOE.
            fab_ps (float): Fabrication pixel size. [mm]
            device (str): Device to run the DOE.
        """
        super().__init__(
            d=d, res=res, wvln0=wvln0, mat=mat, fab_ps=fab_ps, device=device
        )

        # Initial focal length
        if f0 is None:
            self.f0 = torch.randn(1) * 1e6
        else:
            self.f0 = torch.tensor(f0)

        self.to(device)

    @classmethod
    def init_from_dict(cls, doe_dict):
        """Initialize Fresnel DOE from a dict."""
        d = doe_dict["d"]
        res = doe_dict.get("res", (2000, 2000))
        fab_ps = doe_dict.get("fab_ps", 0.001)
        f0 = doe_dict.get("f0", None)
        wvln0 = doe_dict.get("wvln0", 0.55)
        mat = doe_dict.get("mat", "fused_silica")
        return cls(
            d=d,
            res=res,
            fab_ps=fab_ps,
            f0=f0,
            wvln0=wvln0,
            mat=mat,
        )

    def _phase_map0(self):
        """Get the phase map at design wavelength."""
        wvln0_mm = self.wvln0 * 1e-3
        phase = -2 * torch.pi * (self.x**2 + self.y**2) / (2 * self.f0 * wvln0_mm)
        return phase

    # =======================================
    # Optimization
    # =======================================
    def get_optimizer_params(self, lr=0.001):
        """Get parameters for optimization."""
        self.f0.requires_grad = True
        optimizer_params = [{"params": [self.f0], "lr": lr}]
        return optimizer_params

    # =======================================
    # IO
    # =======================================
    def surf_dict(self):
        """Return a dict of surface."""
        surf_dict = super().surf_dict()
        surf_dict["f0"] = self.f0.item()
        surf_dict["wvln0"] = self.wvln0
        return surf_dict
