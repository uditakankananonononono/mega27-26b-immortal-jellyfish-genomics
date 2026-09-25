from jellyfish.cli import main

def test_no_args_shows_help(capsys):
    assert main([]) == 2
    assert "census" in capsys.readouterr().out

def test_unknown_command(capsys):
    assert main(["frobnicate"]) == 2

def test_census(tmp_path, capsys):
    p = tmp_path / "m.fa"
    p.write_text(">c1\n" + "TTAGGG" * 50 + "ACGT" * 1000 + "TTAGGG" * 50 + "\n")
    assert main(["census", str(p)]) == 0
    assert "TTAGGG" in capsys.readouterr().out

def test_compare(tmp_path, capsys):
    q = tmp_path / "q.faa"; q.write_text(">q\nARND\n")
    for i in range(3):
        r = tmp_path / f"r{i}.faa"; r.write_text(f">r{i}\nAGND\n")
    import glob
    assert main(["compare", str(q)] + sorted(glob.glob(str(tmp_path / "r*.faa")))[:3]) == 0
    out = capsys.readouterr().out
    assert "query_pos" in out
