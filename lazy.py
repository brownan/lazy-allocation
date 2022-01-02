from fractions import Fraction
from dataclasses import dataclass
from typing import List

# This dataclass will hold information about each asset. All values are stored
# using the Python Fraction class, which stores rational numbers as two
# arbitrary precision integers in order to avoid arithmetic rounding errors.
@dataclass
class Asset:
    # Actual (current) amount in dollars
    a: Fraction

    # Desired allocation, as a fraction between 0 and 1
    # (all asset allocations should sum to 1)
    d: Fraction

    # Computed target amount in dollars
    t: Fraction = None

    # Computed fractional deviation
    f: Fraction = None

    # Computed amount to add to this asset
    delta: Fraction = None



def lazy_alloc(assets: List[Asset],
               C: Fraction) -> List[Fraction]:
    """The Lazy Asset Allocation Algorithm

    :param assets: A list of Asset objects with the 'actual' and 'allocation'
        values filled in

    :param C: The amount in dollars to contribute

    :returns: The list of 'delta' values, or amount to contribute
        to each asset

    """
    # Compute the 'target' and 'f' values for each asset.
    # Also annotate each asset with its index in the list, so we remember
    # the original asset ordering
    # Values we use are converted into Fraction types if not already.
    T = sum(Fraction(asset.a) for asset in assets) + Fraction(C)
    for asset_index, asset in enumerate(assets):
        # To allow for a desired allocation of 0%, we have to set a minimum
        # target value. A value of exactly 0 for the target would cause a zero
        # division error when calculating the fractional deviation.
        asset.t = T * Fraction(asset.d) or Fraction("0.001")
        asset.f = Fraction(asset.a) / asset.t
        asset.i = asset_index
    C = Fraction(C)

    # Now we can order the assets by their fractional deviation, reversing the
    # direction if we're withdrawing.
    assets.sort(key=lambda asset: asset.f)
    if C < 0:
        assets.reverse()

    # Each loop iteration computes these values for the current step.
    # Note that Python lists are 0-indexed, and we start at step 0.
    # Each loop iteration computes the TC for the current step, but if it
    # exceeds C (or is the last step), then we "back up" and use prev_TC -- the
    # previous step's TC -- to calculate the final fractional deviation.
    step = 0
    r = 0
    prev_TC = 0

    while True:
        # Update this step's fractional deviation and the running total values
        this_f = assets[step].f
        r += assets[step].t

        # First exit condition: if this is the last asset, then exit the loop.
        # If we exit here, it indicates we have more money than required to
        # bring all assets up to the last asset's fractional deviation. The
        # remaining money (C - prev_TC) will be distributed to all assets.
        if step + 1 == len(assets):
            break

        # Calculate the total contributions for the current step, so we can
        # compare it against the contributions.
        next_f = assets[step + 1].f
        TC = prev_TC + r * (next_f - this_f)

        # Second exit condition: TC for the current step exceeds the
        # contributions. We've found the maximum step as described in the
        # equations, which is `step-1`.
        # We compare the absolute values since the signs are inverted when
        # withdrawing.
        if abs(TC) >= abs(C):
            break

        # Increment the loop variables for the next loop iteration
        step += 1
        prev_TC = TC

    # We've exited the loop. The variable `step` has gone one *past* the final
    # step as described in the equations. We therefore use prev_TC to compute
    # the final fractional deviation.
    f_f = this_f + (C - prev_TC) / r

    for asset_index, asset in enumerate(assets):
        # Again since our actual final step is `step-1`, we update all
        # assets <=step (instead of `step+1` as given in the equations)
        if asset_index <= step:
            # Values are rounded to the nearest cent. This could cause the total
            # of all delta values to not sum to the contributions. If this is
            # a problem, take out the round() call for exact answers.
            asset.delta = round(asset.t * (f_f - asset.f), 2)
        else:
            asset.delta = Fraction(0)

    # Re-order the assets to their original ordering
    assets.sort(key=lambda asset: asset.i)

    # And return the delta values
    return [asset.delta for asset in assets]

