# FLASH documentation
This repository hosts the **FLASH** user and developer documentation. It accompanies the Blanchard lab open-source acquisition and analysis tools described in:
**An integrated open-source acquisition and analysis ecosystem for high-throughput single-molecule imaging**  
*Nature Methods* (2026)  
**DOI:** [10.1038/s41592-026-03265-w](https://doi.org/10.1038/s41592-026-03265-w)
Daniel S. Terry, Roman Kiselev, Manuel F. Juette, Zeliha Kilic, Ryan A. Brady, Yuansheng Sun, Scott C. Blanchard  
St. Jude Children’s Research Hospital, Memphis, TN, USA · Weill Cornell Medicine, New York, NY, USA  
Correspondence: [scott.blanchard@stjude.org](mailto:scott.blanchard@stjude.org)
## Links
| Resource | URL |
|----------|-----|
| **Read the manual** | https://stjude-smc.github.io/FLASH_docs/ *(when GitHub Pages is enabled)* |
| **FLASH software** | https://github.com/stjude-smc/FLASH |
## Citation
If you use FLASH or this documentation in your work, **please cite the Nature Methods article** (DOI above), not only the GitHub repository.
Example:
> Terry, D.S., Kiselev, R., Juette, M.F., Kilic, Z., Brady, R.A., Sun, Y. & Blanchard, S.C. An integrated open-source acquisition and analysis ecosystem for high-throughput single-molecule imaging. *Nat. Methods* (2026). https://doi.org/10.1038/s41592-026-03265-w
*(Update author list, volume, and page numbers from the final published PDF when available.)*
## Local build
```bash
pip install -r docs_flash/requirements.txt
cd docs_flash && make html