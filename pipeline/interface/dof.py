# -*- coding: utf-8 -*-
# emacs: -*- mode: python; py-indent-offset: 4; indent-tabs-mode: nil -*-
# vi: set ft=python sts=4 ts=4 sw=4 et:

from os import path as op

import numpy as np
import nibabel as nib

from nipype.interfaces.base import TraitedSpec, BaseInterface, traits, isdefined
from nilearn.image import new_img_like

from ..utils import nvol


class MakeDofVolumeInputSpec(TraitedSpec):
    dof_file = traits.File(desc="", exists=True)
    cope = traits.File(desc="", exists=True)

    bold_file = traits.File(exists=True, desc="input file")
    num_regressors = traits.Range(low=1, desc="number of regressors")


class MakeDofVolumeOutputSpec(TraitedSpec):
    out_file = traits.File(exists=True)


class MakeDofVolume(BaseInterface):
    input_spec = MakeDofVolumeInputSpec
    output_spec = MakeDofVolumeOutputSpec

    def _run_interface(self, runtime):
        self._out_file = None

        dof = None
        ref_img = None

        if isdefined(self.inputs.dof_file):
            with open(self.inputs.dof_file) as file:
                dof = float(file.read())

        if isdefined(self.inputs.bold_file):
            ref_img = nib.load(self.inputs.bold_file)
            if isdefined(self.inputs.num_regressors):
                dof = float(nvol(ref_img) - self.inputs.num_regressors)

        if isdefined(self.inputs.cope_file):
            ref_img = nib.load(self.inputs.cope_file)

        if dof is None:
            return runtime

        if ref_img is None:
            return runtime

        outshape = ref_img.shape
        outarr = np.full(outshape, dof)

        outimg = new_img_like(ref_img, outarr)

        self._out_file = op.abspath(f"dof_file.nii.gz")
        nib.save(outimg, self._out_file)

        return runtime

    def _list_outputs(self):
        outputs = self._outputs().get()

        if self._out_file is not None:
            outputs["out_file"] = op.abspath(self.inputs.out_file)

        return outputs
