from collections.abc import Callable
from pathlib import Path

import pytest

from epicsdb2bob.parser import (
    find_epics_dbs_and_templates,
    order_dbs_by_includes,
    parse_epics_db_file,
)


def test_order_dbs_by_includes_already_in_order(compound_db):
    simple_db, compound_db = compound_db
    ordered_dbs = order_dbs_by_includes({"simple": simple_db, "compound": compound_db})
    assert list(ordered_dbs.keys()) == ["simple", "compound"]


def test_order_dbs_by_includes_out_of_order(compound_db):
    simple_db, compound_db = compound_db
    ordered_dbs = order_dbs_by_includes({"compound": compound_db, "simple": simple_db})
    assert list(ordered_dbs.keys()) == ["simple", "compound"]


def test_parse_epics_db_file_missing_file():
    with pytest.raises(FileNotFoundError):
        parse_epics_db_file(Path("non_existent_file.db"))


@pytest.mark.parametrize(
    "extension",
    [".db", ".template"],
)
def test_parse_epics_db_file(
    simple_db_file_factory: Callable[[int, str], list[Path]], extension
):
    db_files = simple_db_file_factory(1, extension)
    assert len(db_files) == 1
    db_file = db_files[0]

    epics_dbs = parse_epics_db_file(db_file)
    assert len(epics_dbs) == 1
    assert db_file.stem.split(".", -1)[0] in epics_dbs


def test_find_epics_dbs_and_templates_single_file(
    simple_db_file_factory: Callable[[int, str], list[Path]],
):
    db_files = simple_db_file_factory(1, ".db")
    assert len(db_files) == 1
    db_file = db_files[0]

    epics_dbs = find_epics_dbs_and_templates(db_file)
    assert len(epics_dbs) == 1
    assert db_file.stem.split(".", -1)[0] in epics_dbs


def test_find_epics_dbs_and_templates_directory(
    simple_db_file_factory: Callable[[int, str], list[Path]], tmp_path: Path
):
    num_dbs = 3
    db_files = simple_db_file_factory(num_dbs, ".db")
    for db_file in db_files:
        dest = tmp_path / db_file.name
        db_file.rename(dest)

    epics_dbs = find_epics_dbs_and_templates(tmp_path)
    assert len(epics_dbs) == num_dbs
    for db_file in db_files:
        assert db_file.stem.split(".", -1)[0] in epics_dbs


def test_find_epics_dbs_and_templates_compound_db(simple_db, tmp_path: Path):
    with open(tmp_path / "compound.template", "w") as f:
        f.write("include simple.template\n")

    simple_db_file = tmp_path / "simple.template"
    with open(simple_db_file, "w") as f:
        f.write(str(simple_db))

    epics_dbs = find_epics_dbs_and_templates(tmp_path)
    assert len(epics_dbs) == 2
    for i, db in enumerate(epics_dbs):
        if i == 0:
            assert db == "simple"
        elif i == 1:
            assert db == "compound"
