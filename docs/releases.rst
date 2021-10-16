.. _releases:

Making a new release
====================

When making a new release of ``nc-time-axis``, it is best to follow these steps.
Note these are a trimmed-down version of the release steps for the ``Iris``
package, which can be found `here
<https://scitools-iris.readthedocs.io/en/stable/developers_guide/release.html>`_.

1. Create a release branch in the ``SciTools/nc-time-axis`` repository with the
   name ``v{major release number}.{minor release number}.x``.  This branch will
   be used to make any final changes prior to the release.  It will be merged
   back into the ``main`` branch once the release is complete.
2. Check that the :ref:`release_notes` have been fully updated for the new
   release. This includes adding a date for the new release where it currently
   says "unreleased."  This can also include formatting and other minor content
   updates.
3. `Create a new tag in the GitHub
   <https://github.com/SciTools/nc-time-axis/releases/new>`_ repository for the
   new release.  This should have the same name as the release branch.
4. Update the conda-forge feedstock for the new release.  This involves making a
   pull request to the `conda-forge/nc_time_axis-feedstock
   <https://github.com/conda-forge/nc_time_axis-feedstock>`_ repository in which
   the ``version`` and ``sha256`` are updated in the ``recipe/meta.yaml`` file.
   The ``version`` should correspond to the new version of the release, and the
   ``sha256`` can be generated using the ``openssl`` tool as described `in the
   tip in the conda-forge documentation
   <https://conda-forge.org/docs/maintainer/adding_pkgs.html#step-by-step-instructions>`_::

      curl -sL https://pypi.io/packages/source/n/nc-time-axis/nc-time-axis-vX.Y.Z.tar.gz | openssl sha256

   Follow the checklist in the PR template, request reviews if necessary, and
   then merge the PR.
5. Upload the release to `PyPI <https://pypi.org>`_.  You can follow the
   instructions `here
   <https://scitools-iris.readthedocs.io/en/stable/developers_guide/release.html#update-pypi>`_.
6. Ensure the documentation has been built properly on `Read the Docs
   <https://readthedocs.org>`_ and that the new release is an "active version."
7. Update the :ref:`release_notes` page to include a blank section for the next
   release.
8. Merge the release branch into ``main``, but leave it available in case any
   point releases are needed.
