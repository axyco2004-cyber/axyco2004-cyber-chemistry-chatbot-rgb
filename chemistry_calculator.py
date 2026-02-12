"""
Chemistry Calculator Module
Provides calculation functions for stoichiometry, solutions, pH, gas laws, and more.
"""

import math
import re
import periodictable


class ChemistryCalculator:
    """Chemistry problem solver with various calculation methods."""
    
    # Constants
    AVOGADRO = 6.022e23  # Avogadro's number (molecules/mol)
    GAS_CONSTANT = 0.0821  # L·atm/(mol·K)
    
    def __init__(self):
        pass
    
    # ==================== STOICHIOMETRY ====================
    
    def moles_to_grams(self, formula: str, moles: float) -> dict:
        """Convert moles to grams."""
        try:
            molar_mass = periodictable.formula(formula).mass
            grams = moles * molar_mass
            return {
                "formula": formula,
                "moles": moles,
                "grams": round(grams, 4),
                "molar_mass": round(molar_mass, 4)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def grams_to_moles(self, formula: str, grams: float) -> dict:
        """Convert grams to moles."""
        try:
            molar_mass = periodictable.formula(formula).mass
            moles = grams / molar_mass
            return {
                "formula": formula,
                "grams": grams,
                "moles": round(moles, 4),
                "molar_mass": round(molar_mass, 4)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def moles_to_molecules(self, moles: float) -> dict:
        """Convert moles to molecules."""
        try:
            molecules = moles * self.AVOGADRO
            return {
                "moles": moles,
                "molecules": f"{molecules:.3e}",
                "avogadro": f"{self.AVOGADRO:.3e}"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def molecules_to_moles(self, molecules: float) -> dict:
        """Convert molecules to moles."""
        try:
            moles = molecules / self.AVOGADRO
            return {
                "molecules": f"{molecules:.3e}",
                "moles": round(moles, 6),
                "avogadro": f"{self.AVOGADRO:.3e}"
            }
        except Exception as e:
            return {"error": str(e)}
    
    # ==================== SOLUTION CHEMISTRY ====================
    
    def calculate_molarity(self, moles: float = None, grams: float = None, 
                          formula: str = None, volume_L: float = None) -> dict:
        """Calculate molarity (M = mol/L)."""
        try:
            if moles is None and grams is not None and formula is not None:
                molar_mass = periodictable.formula(formula).mass
                moles = grams / molar_mass
            
            if moles is None or volume_L is None:
                return {"error": "Need moles (or grams + formula) and volume in liters"}
            
            molarity = moles / volume_L
            
            return {
                "moles": round(moles, 4),
                "volume_L": volume_L,
                "molarity": round(molarity, 4),
                "formula": formula if formula else "N/A"
            }
        except Exception as e:
            return {"error": str(e)}
    
    def dilution(self, M1: float, V1: float, M2: float = None, V2: float = None) -> dict:
        """Calculate dilution using M1V1 = M2V2."""
        try:
            if M2 is None and V2 is not None:
                M2 = (M1 * V1) / V2
                return {
                    "initial_molarity": M1,
                    "initial_volume": V1,
                    "final_volume": V2,
                    "final_molarity": round(M2, 4),
                    "formula": "M1V1 = M2V2"
                }
            elif V2 is None and M2 is not None:
                V2 = (M1 * V1) / M2
                return {
                    "initial_molarity": M1,
                    "initial_volume": V1,
                    "final_molarity": M2,
                    "final_volume": round(V2, 4),
                    "formula": "M1V1 = M2V2"
                }
            else:
                return {"error": "Need M1, V1, and either M2 or V2"}
        except Exception as e:
            return {"error": str(e)}
    
    # ==================== pH CALCULATIONS ====================
    
    def calculate_pH(self, H_concentration: float) -> dict:
        """Calculate pH from H+ concentration."""
        try:
            if H_concentration <= 0:
                return {"error": "H+ concentration must be positive"}
            
            pH = -math.log10(H_concentration)
            pOH = 14 - pH
            OH_concentration = 10 ** (-pOH)
            
            return {
                "H_concentration": f"{H_concentration:.3e}",
                "pH": round(pH, 2),
                "pOH": round(pOH, 2),
                "OH_concentration": f"{OH_concentration:.3e}",
                "nature": "Acidic" if pH < 7 else ("Neutral" if pH == 7 else "Basic")
            }
        except Exception as e:
            return {"error": str(e)}
    
    def calculate_pOH(self, OH_concentration: float) -> dict:
        """Calculate pOH from OH- concentration."""
        try:
            if OH_concentration <= 0:
                return {"error": "OH- concentration must be positive"}
            
            pOH = -math.log10(OH_concentration)
            pH = 14 - pOH
            H_concentration = 10 ** (-pH)
            
            return {
                "OH_concentration": f"{OH_concentration:.3e}",
                "pOH": round(pOH, 2),
                "pH": round(pH, 2),
                "H_concentration": f"{H_concentration:.3e}",
                "nature": "Acidic" if pH < 7 else ("Neutral" if pH == 7 else "Basic")
            }
        except Exception as e:
            return {"error": str(e)}
    
    def pH_from_value(self, pH: float) -> dict:
        """Get all pH-related values from pH."""
        try:
            if pH < 0 or pH > 14:
                return {"error": "pH must be between 0 and 14"}
            
            H_concentration = 10 ** (-pH)
            pOH = 14 - pH
            OH_concentration = 10 ** (-pOH)
            
            return {
                "pH": pH,
                "pOH": round(pOH, 2),
                "H_concentration": f"{H_concentration:.3e}",
                "OH_concentration": f"{OH_concentration:.3e}",
                "nature": "Acidic" if pH < 7 else ("Neutral" if pH == 7 else "Basic")
            }
        except Exception as e:
            return {"error": str(e)}
    
    # ==================== GAS LAWS ====================
    
    def ideal_gas_law(self, P: float = None, V: float = None, n: float = None, 
                      T: float = None) -> dict:
        """Calculate using PV = nRT. Solve for the missing variable."""
        try:
            R = self.GAS_CONSTANT
            
            # Count how many variables are provided
            provided = sum([x is not None for x in [P, V, n, T]])
            
            if provided != 3:
                return {"error": "Provide exactly 3 variables (P, V, n, or T). Units: P(atm), V(L), n(mol), T(K)"}
            
            if P is None:
                P = (n * R * T) / V
                return {"P_atm": round(P, 4), "V_L": V, "n_mol": n, "T_K": T, "R": R, "solved_for": "P"}
            elif V is None:
                V = (n * R * T) / P
                return {"P_atm": P, "V_L": round(V, 4), "n_mol": n, "T_K": T, "R": R, "solved_for": "V"}
            elif n is None:
                n = (P * V) / (R * T)
                return {"P_atm": P, "V_L": V, "n_mol": round(n, 4), "T_K": T, "R": R, "solved_for": "n"}
            elif T is None:
                T = (P * V) / (n * R)
                return {"P_atm": P, "V_L": V, "n_mol": n, "T_K": round(T, 4), "R": R, "solved_for": "T"}
        except Exception as e:
            return {"error": str(e)}
    
    def combined_gas_law(self, P1: float = None, V1: float = None, T1: float = None,
                        P2: float = None, V2: float = None, T2: float = None) -> dict:
        """Calculate using (P1V1)/T1 = (P2V2)/T2."""
        try:
            # Count variables in each state
            state1 = sum([x is not None for x in [P1, V1, T1]])
            state2 = sum([x is not None for x in [P2, V2, T2]])
            
            if state1 + state2 != 5:
                return {"error": "Provide 5 out of 6 variables. Units: P(atm), V(L), T(K)"}
            
            if P2 is None:
                P2 = (P1 * V1 * T2) / (T1 * V2)
                return {"P1": P1, "V1": V1, "T1": T1, "P2": round(P2, 4), "V2": V2, "T2": T2, "solved_for": "P2"}
            elif V2 is None:
                V2 = (P1 * V1 * T2) / (T1 * P2)
                return {"P1": P1, "V1": V1, "T1": T1, "P2": P2, "V2": round(V2, 4), "T2": T2, "solved_for": "V2"}
            elif T2 is None:
                T2 = (P2 * V2 * T1) / (P1 * V1)
                return {"P1": P1, "V1": V1, "T1": T1, "P2": P2, "V2": V2, "T2": round(T2, 4), "solved_for": "T2"}
            elif P1 is None:
                P1 = (P2 * V2 * T1) / (V1 * T2)
                return {"P1": round(P1, 4), "V1": V1, "T1": T1, "P2": P2, "V2": V2, "T2": T2, "solved_for": "P1"}
            elif V1 is None:
                V1 = (P2 * V2 * T1) / (P1 * T2)
                return {"P1": P1, "V1": round(V1, 4), "T1": T1, "P2": P2, "V2": V2, "T2": T2, "solved_for": "V1"}
            elif T1 is None:
                T1 = (P1 * V1 * T2) / (P2 * V2)
                return {"P1": P1, "V1": V1, "T1": round(T1, 4), "P2": P2, "V2": V2, "T2": T2, "solved_for": "T1"}
        except Exception as e:
            return {"error": str(e)}
    
    # ==================== PERCENT COMPOSITION ====================
    
    def percent_composition(self, formula: str) -> dict:
        """Calculate mass percent of each element in a compound."""
        try:
            compound = periodictable.formula(formula)
            total_mass = compound.mass
            
            # Get element composition
            element_masses = {}
            for element, count in compound.atoms.items():
                element_mass = element.mass * count
                percent = (element_mass / total_mass) * 100
                element_masses[element.symbol] = {
                    "count": count,
                    "mass": round(element_mass, 4),
                    "percent": round(percent, 2)
                }
            
            return {
                "formula": formula,
                "total_mass": round(total_mass, 4),
                "elements": element_masses
            }
        except Exception as e:
            return {"error": str(e)}
    
    # ==================== LIMITING REACTANT ====================
    
    def limiting_reactant(self, reactant1_formula: str, reactant1_grams: float,
                         reactant1_coef: int, reactant2_formula: str,
                         reactant2_grams: float, reactant2_coef: int) -> dict:
        """Determine limiting reactant and theoretical yield."""
        try:
            # Calculate moles of each reactant
            molar_mass1 = periodictable.formula(reactant1_formula).mass
            molar_mass2 = periodictable.formula(reactant2_formula).mass
            
            moles1 = reactant1_grams / molar_mass1
            moles2 = reactant2_grams / molar_mass2
            
            # Calculate moles available per coefficient (stoichiometric ratio)
            ratio1 = moles1 / reactant1_coef
            ratio2 = moles2 / reactant2_coef
            
            if ratio1 < ratio2:
                limiting = reactant1_formula
                limiting_moles = moles1
                excess = reactant2_formula
                excess_moles = moles2
            else:
                limiting = reactant2_formula
                limiting_moles = moles2
                excess = reactant1_formula
                excess_moles = moles1
            
            return {
                "reactant1": {
                    "formula": reactant1_formula,
                    "grams": reactant1_grams,
                    "moles": round(moles1, 4),
                    "coefficient": reactant1_coef,
                    "ratio": round(ratio1, 4)
                },
                "reactant2": {
                    "formula": reactant2_formula,
                    "grams": reactant2_grams,
                    "moles": round(moles2, 4),
                    "coefficient": reactant2_coef,
                    "ratio": round(ratio2, 4)
                },
                "limiting_reactant": limiting,
                "excess_reactant": excess
            }
        except Exception as e:
            return {"error": str(e)}


# Global instance for easy import
calculator = ChemistryCalculator()
