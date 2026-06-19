import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.widgets import RadioButtons

def run(results):
    """
    Harmonic spectrum analysis for a single-phase full-wave thyristor bridge rectifier.
    Uses FFT to compute ALL harmonics (1st to 20th) as a percentage of V_dc,
    plus THD and ripple factor, for each firing angle in the results list.
    Odd harmonics will be near-zero for a symmetric circuit; any non-zero
    odd content reveals real asymmetry in the measured circuit.
    Displays an interactive matplotlib plot with RadioButtons to switch between angles.
    """

    MAX_HARMONIC = 20                               # Analyse up to the 20th harmonic
    ALL_ORDERS   = list(range(1, MAX_HARMONIC + 1)) # [1, 2, 3, ..., 20]
    N_SAMPLES    = 10000                            # Waveform resolution — higher = more accurate FFT

    # ------------------------------------------------------------------
    # Rebuild V_m from the USER-measured voltage and firing angle,
    # so the spectrum reflects actual lab results, not ideal theory.
    # V_dc = (Vm/π)(1 + cosα)  →  Vm = V_dc · π / (1 + cosα)
    # Special case α = 180°: 1 + cos(180°) = 0, so V_dc = 0 and
    # harmonics are undefined; we skip that entry gracefully.
    # ------------------------------------------------------------------

    def compute_spectrum(V_dc, V_m, alpha):
        """
        Synthesises one full cycle of the rectified waveform, runs an FFT,
        and extracts harmonic amplitudes for all orders 1..MAX_HARMONIC.

        For a perfect symmetric full-wave rectifier, odd harmonics will be
        essentially zero (numerical noise only). Any non-zero odd content
        reflects real circuit asymmetry in a lab measurement.

        Returns a dict with:
          harmonics : {order: {"volts": V_n, "pct": amplitude_%}}
                      for all orders 1..MAX_HARMONIC
          thd       : total harmonic distortion (%) — excludes DC and fundamental
          ripple    : ripple factor (%)
        """
        if V_dc == 0:
            return None

        # ------------------------------------------------------------------
        # Step 1 — Synthesise the rectified waveform over one supply cycle.
        # The thyristor conducts from α to π each half-cycle, producing a
        # clipped half-sinusoid: zero before α, |Vm·sin(θ)| from α to π.
        # np.where applies this condition sample-by-sample across the cycle.
        # ------------------------------------------------------------------
        theta    = np.linspace(0, 2 * np.pi, N_SAMPLES, endpoint=False)
        waveform = np.where(theta % np.pi >= alpha, V_m * np.abs(np.sin(theta)), 0.0)

        # ------------------------------------------------------------------
        # Step 2 — FFT.
        # np.fft.rfft returns the one-sided complex spectrum (DC to Nyquist).
        # Scaling by 2/N converts raw FFT bins to peak amplitudes;
        # the DC bin (index 0) needs only 1/N so we halve it after.
        # ------------------------------------------------------------------
        fft_raw    = np.fft.rfft(waveform)
        amplitudes = (2.0 / N_SAMPLES) * np.abs(fft_raw)
        amplitudes[0] /= 2  # correct DC bin scaling

        # ------------------------------------------------------------------
        # Step 3 — Extract harmonics 1..MAX_HARMONIC.
        # FFT bin k corresponds directly to the k-th harmonic of the
        # fundamental, so harmonic n sits at index n.
        # THD excludes the DC component (n=0) and the fundamental (n=1).
        # ------------------------------------------------------------------
        harmonics = {}
        sum_sq    = 0.0

        for n in ALL_ORDERS:
            V_n = float(amplitudes[n]) if n < len(amplitudes) else 0.0
            pct = (V_n / V_dc) * 100
            harmonics[n] = {"volts": V_n, "pct": pct}
            if n > 1:                   # THD excludes the fundamental
                sum_sq += V_n ** 2

        thd    = (math.sqrt(sum_sq) / V_dc) * 100
        ripple = thd  # identical for resistive load

        return {
            "harmonics": harmonics,
            "thd":       thd,
            "ripple":    ripple
        }

    # ------------------------------------------------------------------
    # Build per-angle spectrum data
    # ------------------------------------------------------------------
    angle_data = {}  # keyed by label string, e.g. "α = 30.0°"

    for r in results:
        alpha_deg = r["firing_angle"]
        alpha     = math.radians(alpha_deg)
        V_dc      = r["user_voltage"]   # Use measured voltage, not ideal

        denom = 1 + math.cos(alpha)
        if abs(denom) < 1e-9 or V_dc < 1e-9:
            print(f"  [Harmonics] Skipping α = {alpha_deg}° (V_dc ≈ 0, harmonics undefined).")
            continue

        V_m      = V_dc * math.pi / denom   # Reconstruct Vm from measured V_dc
        spectrum = compute_spectrum(V_dc, V_m, alpha)

        if spectrum is None:
            continue

        label = f"α = {alpha_deg:.1f}°"
        angle_data[label] = {
            "alpha_deg": alpha_deg,
            "V_dc":      V_dc,
            "spectrum":  spectrum
        }

    if not angle_data:
        print("No valid firing angles available for harmonic analysis.")
        return

    labels = list(angle_data.keys())

    # ------------------------------------------------------------------
    # Plot layout:
    #   Left  : RadioButtons (angle selector)
    #   Right : Bar chart + annotation text
    # ------------------------------------------------------------------
    fig = plt.figure(figsize=(13, 6))
    fig.patch.set_facecolor("#1a1a2e")

    gs = gridspec.GridSpec(1, 3, width_ratios=[1, 4, 1.2], wspace=0.08)

    ax_radio = fig.add_subplot(gs[0])
    ax_radio.set_facecolor("#16213e")
    ax_radio.set_title("Firing Angle", color="white", fontsize=10, pad=8)

    ax_bar = fig.add_subplot(gs[1])
    ax_bar.set_facecolor("#0f3460")

    ax_info = fig.add_subplot(gs[2])
    ax_info.set_facecolor("#16213e")
    ax_info.axis("off")  # no axes — used purely as a text canvas

    # Style helper
    def style_axes(ax):
        ax.tick_params(colors="white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.title.set_color("white")
        for spine in ax.spines.values():
            spine.set_edgecolor("#444466")

    style_axes(ax_bar)

    # ------------------------------------------------------------------
    # Draw function — called on first render and on every radio click
    # ------------------------------------------------------------------
    info_text = {"obj": None}  # mutable container so the closure can update it

    def draw(label):
        ax_bar.cla()
        ax_bar.set_facecolor("#0f3460")
        style_axes(ax_bar)

        entry    = angle_data[label]
        spectrum = entry["spectrum"]
        V_dc     = entry["V_dc"]
        orders   = ALL_ORDERS
        pcts     = [spectrum["harmonics"][n]["pct"]   for n in orders]
        volts    = [spectrum["harmonics"][n]["volts"] for n in orders]

        # Colour bars by harmonic type and magnitude:
        #   Even harmonics — expected, colour by magnitude (red > 10%, teal <= 10%)
        #   Odd harmonics  — unexpected, always shown in amber as a warning
        colours = []
        for n, p in zip(orders, pcts):
            if n % 2 == 0:
                colours.append("#e94560" if p > 10 else "#0f9b8e")  # red / teal
            else:
                colours.append("#f5a623")                            # amber — odd harmonic

        bars = ax_bar.bar(
            [str(n) for n in orders],
            pcts,
            color=colours,
            edgecolor="#1a1a2e",
            linewidth=0.8,
            width=0.6
        )

        # DC reference line — bright cyan so it's distinct from the amber odd-harmonic bars
        ax_bar.axhline(100, color="#00d4ff", linewidth=1.5,
                       linestyle="--", label=f"V_dc (measured) = {V_dc:.2f} V (100%)")

        # Inline label just below the dashed line on the right side
        ax_bar.text(
            0.99, 100 - 1.5,
            f"{V_dc:.2f} V",
            transform=ax_bar.get_yaxis_transform(),
            ha="right", va="top",
            color="#00d4ff", fontsize=9, fontstyle="italic"
        )

        # Legend patches to explain the colour scheme
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor="#e94560", label="Even harmonic  > 10% (significant)"),
            Patch(facecolor="#0f9b8e", label="Even harmonic <= 10% (minor)"),
            Patch(facecolor="#f5a623", label="Odd harmonic (asymmetry indicator)"),
        ]
        ax_bar.legend(
            handles=legend_elements,
            facecolor="#1a1a2e", labelcolor="white", fontsize=8,
            loc="upper right", bbox_to_anchor=(1.0, 0.72)
        )

        # Value labels on top of each bar — show both voltage and percentage
        for bar, pct, v in zip(bars, pcts, volts):
            if pct > 0.5:
                ax_bar.text(
                    bar.get_x() + bar.get_width() / 2,
                    bar.get_height() + 0.4,
                    f"{v:.2f} V\n{pct:.1f}%",
                    ha="center", va="bottom",
                    color="white", fontsize=7.5,
                    linespacing=1.4
                )

        ax_bar.set_xlabel("Harmonic Order", fontsize=11)
        ax_bar.set_ylabel("Amplitude (% of V_dc)", fontsize=11)
        ax_bar.set_title(
            f"Harmonic Spectrum — {label}  |  All harmonics 1st-{MAX_HARMONIC}th  |  Measured data",
            fontsize=12, pad=10
        )

        # THD / ripple + per-harmonic table in annotation box
        thd    = spectrum["thd"]
        ripple = spectrum["ripple"]

        lines = [
            f"THD           = {thd:.2f}%",
            f"Ripple Factor = {ripple:.2f}%",
            "",
            f"{'Order':<7} {'Volts':>8} {'% of Vdc':>10}",
            "-" * 30,
        ]
        for n, v, p in zip(orders, volts, pcts):
            tag = "  <- odd" if n % 2 != 0 and p > 0.5 else ""
            lines.append(f"{n:<7} {v:>7.3f} V  {p:>8.2f}%{tag}")

        ann = "\n".join(lines)

        if info_text["obj"] is not None:
            try:
                info_text["obj"].remove()
            except Exception:
                pass

        ax_info.cla()
        ax_info.set_facecolor("#16213e")
        ax_info.axis("off")

        info_text["obj"] = ax_info.text(
            0.05, 0.97, ann,
            transform=ax_info.transAxes,
            fontsize=8, color="white",
            verticalalignment="top",
            horizontalalignment="left",
            family="monospace",
            bbox=dict(boxstyle="round,pad=0.5", facecolor="#2a2a4a",
                      edgecolor="#7777aa", alpha=0.95)
        )

        fig.canvas.draw_idle()

    # ------------------------------------------------------------------
    # Radio buttons
    # ------------------------------------------------------------------
    radio = RadioButtons(
        ax_radio,
        labels,
        activecolor="#e94560"
    )

    # Style the radio labels
    for lbl in radio.labels:
        lbl.set_color("white")
        lbl.set_fontsize(9)

    radio.on_clicked(draw)

    # Initial render
    draw(labels[0])

    plt.suptitle(
        "Single-Phase Full-Wave Thyristor Rectifier — EMI Harmonic Analysis",
        color="white", fontsize=13, y=0.98
    )

    plt.tight_layout()
    plt.show()