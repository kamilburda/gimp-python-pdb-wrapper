1.3
===

* Arguments to PDB procedures are now automatically wrapped with `GObject.Value()`.
* Updated the stub file to remove `GObject.Value` as an accepted type for PDB arguments.

1.2
===

* Prevented errors when importing the `pypdb` module when GIMP is not fully initialized.


1.1
===

* Allowed access to PDB procedures via strings as `pdb['some-procedure-name']`.
* Python exceptions are now raised if attempting to access non-existent procedure names.


1.0
===

* Initial release.
