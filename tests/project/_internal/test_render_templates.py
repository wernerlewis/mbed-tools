#
# Copyright (c) 2020-2021 Arm Limited and Contributors. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest import mock
import logging

from mbed_tools.project._internal.render_templates import (
    render_cmakelists_template,
    render_main_cpp_template,
    render_gitignore_template,
)


MBED_OS_TEMPLATE_PATH = Path("mbed-os", "tools", "cmake", "CMakeLists.tmpl")


@mock.patch("mbed_tools.project._internal.render_templates.datetime")
class TestRenderTemplates:
    def test_renders_cmakelists_template_local_default(self, mock_datetime, caplog):
        caplog.set_level(logging.DEBUG)
        with TemporaryDirectory() as tmpdir:
            the_year = 3999
            mock_datetime.datetime.now.return_value.year = the_year
            program_name = "mytestprogram"
            file_path = Path(tmpdir, "mytestpath")

            render_cmakelists_template(file_path, program_name)
            output = file_path.read_text()

            assert str(the_year) in output
            assert program_name in output
            assert "Using local template from tools." in caplog.text

    def test_renders_cmakelists_template_from_os(self, mock_datetime, caplog):
        caplog.set_level(logging.DEBUG)
        with TemporaryDirectory() as tmpdir:
            the_year = 3999
            tmpl_path = Path(tmpdir, MBED_OS_TEMPLATE_PATH)
            tmpl_path.parent.mkdir(parents=True, exist_ok=True)
            tmpl_path.touch(exist_ok=True)
            tmpl_path.write_text("{{year}} {{program_name}}\n")

            mock_datetime.datetime.now.return_value.year = the_year
            program_name = "mytestprogram"
            file_path = Path(tmpdir, "mytestpath")

            render_cmakelists_template(file_path, program_name, tmpl_path)
            output = file_path.read_text()

            assert f"{the_year} {program_name}" in output
            assert "Template found in Mbed OS" in caplog.text
            assert "Using local copy " not in caplog.text

    def test_renders_main_cpp_template(self, mock_datetime):
        with TemporaryDirectory() as tmpdir:
            the_year = 3999
            mock_datetime.datetime.now.return_value.year = the_year
            file_path = Path(tmpdir, "mytestpath")

            render_main_cpp_template(file_path)

            assert str(the_year) in file_path.read_text()

    def test_renders_gitignore_template(self, _):
        with TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir, "mytestpath")

            render_gitignore_template(file_path)

            assert "cmake_build" in file_path.read_text()
            assert ".mbedbuild" in file_path.read_text()
