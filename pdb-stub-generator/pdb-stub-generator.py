#!/usr/bin/env python3

"""GIMP plug-in that provides a convenience wrapper for invoking GIMP PDB procedures and generates
stubs for PDB procedures to allow displaying code completion suggestions in IDEs.
"""

import sys

import gi
gi.require_version('Gimp', '3.0')
from gi.repository import Gimp
from gi.repository import GObject
from gi.repository import GLib

import stubgen_pdb


def generate_pdb_stubs(run_mode, output_filepath=stubgen_pdb.STUB_MODULE_FILEPATH):
  if not output_filepath:
    output_filepath = stubgen_pdb.STUB_MODULE_FILEPATH

  stubgen_pdb.generate_pdb_stubs(output_filepath)


def _value_array_to_list(array):
  return [array.index(i) for i in range(array.length())]


class PdbStubGenerator(Gimp.PlugIn):
    @GObject.Property(
      type=Gimp.RunMode,
      default=Gimp.RunMode.NONINTERACTIVE,
      nick='Run mode',
      blurb='The run mode')
    def run_mode(self):
      return self._run_mode

    @run_mode.setter
    def run_mode(self, run_mode):
      self._run_mode = run_mode

    @GObject.Property(
      type=str,
      default=stubgen_pdb.STUB_MODULE_FILEPATH,
      nick='Output file path',
      blurb=f'Output file path (default: "{stubgen_pdb.STUB_MODULE_FILEPATH}")',
      flags=GObject.ParamFlags.READWRITE)
    def output_filepath(self):
      return self._output_filepath

    @output_filepath.setter
    def output_filepath(self, value):
      self._output_filepath = value

    def do_set_i18n(self, name):
      return False

    def do_query_procedures(self):
      return ['generate-pdb-stubs']

    def do_create_procedure(self, name):
      procedure = Gimp.Procedure.new(
        self,
        name,
        Gimp.PDBProcType.PLUGIN,
        self.run,
        None)

      procedure.set_image_types('')
      procedure.set_documentation(
        'Generates a stub file for the GIMP procedural database (PDB) for Python.',
        'The stub can then be used in IDEs to display code completion suggestions.',
        name)
      procedure.set_menu_label('Generate GIMP PDB Stubs for Python')
      procedure.set_attribution('Kamil Burda', '', '2023')
      procedure.add_menu_path('<Image>/Filters/Development/Python-Fu')

      procedure.add_argument_from_property(self, 'run-mode')
      procedure.add_argument_from_property(self, 'output-filepath')

      return procedure

    @staticmethod
    def run(procedure, args, data):
      run_mode = args.index(0)

      config = procedure.create_config()
      config.begin_run(None, run_mode, args)
      config.get_values(args)

      generate_pdb_stubs(run_mode, *_value_array_to_list(args)[1:])

      config.end_run(Gimp.PDBStatusType.SUCCESS)

      return procedure.new_return_values(Gimp.PDBStatusType.SUCCESS, GLib.Error())


Gimp.main(PdbStubGenerator.__gtype__, sys.argv)
