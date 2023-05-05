from game import Game

def test_saveScore(tmpdir):
    data_in = "13213"
    fpath = f"{tmpdir}/test.txt"
    Game.saveScore(fpath,data_in)

    with open(fpath) as file_out:
        data_out = file_out.read()
    assert data_in == 'data_out'