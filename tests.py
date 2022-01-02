from unittest import TestCase
from fractions import Fraction

from lazy import lazy_alloc, Asset

class TestLazy(TestCase):

    def assert_deltas(self, assets, deltas):
        self.assertEqual(
            [Fraction(d) for d in deltas],
            [a.delta for a in assets],
        )

    def test_one(self):
        """Two assets equal desired weight, add exactly enough
        to bring the underweighted up to the other

        """
        assets = [
            Asset(Fraction(100), Fraction("0.5")),
            Asset(Fraction(200), Fraction("0.5")),
        ]
        lazy_alloc(assets, Fraction(100))
        self.assert_deltas(
            assets,
            [100, 0]
        )

    def test_two(self):
        """Two assets equal desired weight, add enough to bring them up to
        equal, then a bit more, which should be divided evenly"""
        assets = [
            Asset(Fraction(100), Fraction("0.5")),
            Asset(Fraction(200), Fraction("0.5")),
        ]
        lazy_alloc(assets, Fraction(110))
        self.assert_deltas(
            assets,
            [105, 5]
        )

    def test_three(self):
        """Two assets equal desired weight, but not enough contributions
        to bring it equal. All contributions should go into the one"""
        assets = [
            Asset(Fraction(100), Fraction("0.5")),
            Asset(Fraction(200), Fraction("0.5")),
        ]
        lazy_alloc(assets, Fraction(50))
        self.assert_deltas(
            assets,
            [50, 0]
        )

    def test_four(self):
        """Two assets, and more money is given than required"""
        assets = [
            Asset(Fraction(100), Fraction("0.5")),
            Asset(Fraction(200), Fraction("0.5")),
        ]
        lazy_alloc(assets, Fraction(500))
        self.assert_deltas(
            assets,
            [300, 200]
        )

    def test_five(self):
        assets = [
            Asset(Fraction(9000), Fraction("0.55")),
            Asset(Fraction(4000), Fraction("0.30")),
            Asset(Fraction(3500), Fraction("0.15")),
        ]
        lazy_alloc(assets, Fraction(2000))
        self.assert_deltas(
            assets,
            [Fraction("705.88"), Fraction("1294.12"), 0]
        )

    def test_six(self):
        assets = [
            Asset(Fraction(9000), Fraction("0.55")),
            Asset(Fraction(4000), Fraction("0.30")),
            Asset(Fraction(3500), Fraction("0.15")),
        ]
        lazy_alloc(assets, Fraction(10000))
        self.assert_deltas(
            assets,
            [Fraction("5575.00"), Fraction("3950.00"), Fraction("475.00")]
        )

    def test_w_one(self):
        """Tests withdraws, equal withdraw from each"""
        assets = [
            Asset(Fraction(100), Fraction(0.5)),
            Asset(Fraction(100), Fraction(0.5)),
        ]
        lazy_alloc(
            assets,
            Fraction(-100),
        )
        self.assert_deltas(
            assets,
            [Fraction(-50), Fraction(-50)],
        )

    def test_w_two(self):
        """Tests withdraws, some from one, then equal from both"""
        assets = [
            Asset(Fraction(150), Fraction(0.5)),
            Asset(Fraction(100), Fraction(0.5)),
        ]
        lazy_alloc(
            assets,
            Fraction(-100),
        )
        self.assert_deltas(
            assets,
            [Fraction(-75), Fraction(-25)],
        )

    def test_w_three(self):
        assets = [
            Asset(Fraction(9000), Fraction("0.55")),
            Asset(Fraction(4000), Fraction("0.30")),
            Asset(Fraction(3500), Fraction("0.15")),
        ]
        lazy_alloc(assets, Fraction(-10000))
        self.assert_deltas(
            assets,
            [Fraction("-5425"), Fraction("-2050"), Fraction("-2525")]
        )

    def test_w_four(self):
        assets = [
            Asset(Fraction(1000), Fraction(0.33)),
            Asset(Fraction(2000), Fraction(0.33)),
            Asset(Fraction(3000), Fraction(0.33)),
        ]
        lazy_alloc(assets, Fraction(-3000))
        self.assert_deltas(
            assets,
            [Fraction(0), Fraction("-1000"), Fraction("-2000")]
        )

    def test_not_normalized(self):
        assets = [
            Asset(Fraction(100), Fraction(0.2)),
            Asset(Fraction(200), Fraction(0.2)),
            Asset(Fraction(100), Fraction(0.2)),
        ]
        lazy_alloc(assets, Fraction(300))
        self.assert_deltas(
            assets,
            [Fraction("133.33"), Fraction("33.33"), Fraction("133.33")]
        )

    def test_withdraw_not_normalized(self):
        assets = [
            Asset(Fraction(100), Fraction(0.2)),
            Asset(Fraction(200), Fraction(0.2)),
            Asset(Fraction(100), Fraction(0.2)),
        ]
        lazy_alloc(assets, Fraction(-300))
        self.assert_deltas(
            assets,
            [Fraction("-66.67"), Fraction("-166.67"), Fraction("-66.67")]
        )

    def test_zero_alloc(self):
        assets = [
            Asset(Fraction(100), Fraction(1)),
            Asset(Fraction(100), Fraction(0)),
        ]
        lazy_alloc(assets, Fraction(10))
        self.assert_deltas(
            assets,
            [Fraction(10), Fraction(0)]
        )

    def test_zero_withdraw(self):
        assets = [
            Asset(Fraction(100), Fraction(1)),
            Asset(Fraction(100), Fraction(0)),
        ]
        lazy_alloc(assets, Fraction(-10))
        self.assert_deltas(
            assets,
            [Fraction(0), Fraction(-10)]
        )

    def test_zero_withdraw_two(self):
        assets = [
            Asset(Fraction(100), Fraction(0)),
            Asset(Fraction(100), Fraction(0.5)),
            Asset(Fraction(100), Fraction(0.5)),
        ]
        lazy_alloc(assets, Fraction(-150))
        self.assert_deltas(
            assets,
            [Fraction(-100), Fraction(-25), Fraction(-25)]
        )
