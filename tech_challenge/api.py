from fastapi import FastAPI, Depends, HTTPException, status, Path, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from typing import Optional
from datetime import timedelta
import uvicorn
# import os
from .utils.segment_enum import Segment
from .utils.processing_sub_option_enum import ProcessingSubOption
from .utils.sub_option_enum import SubOption
from .scraper import get_available_years, get_products
from .utils.jwt_utils import create_access_token, get_current_user, ACCESS_TOKEN_EXPIRE_MINUTES

# # Importar suas classes e funções
# from .utils.product import Product
# from .utils.scraper import get_available_years, convert_table_in_object

app = FastAPI(
    title="VITINIGPT - Dados da Vitivinicultura Gaúcha",
    description="API para acesso aos dados estatísticos da produção, comercialização e processamento de uvas, vinhos e derivados do estado do Rio Grande do Sul.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, restrinja isso
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Solicite acesso a documentação."}

@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Simplificado - em um caso real, você verificaria as credenciais
    if form_data.username == "techChallenge01" and form_data.password == "Fiap#2025":
        token_data = {"sub": form_data.username}
        access_token = create_access_token(
            data=token_data,
            expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais incorretas",
            headers={"WWW-Authenticate": "Bearer"},
        )

@app.get("/years/{segment}")
async def get_years_by_segment(
    segment: str = Path(..., description="Nome do segmento (PRODUCTION, PROCESSING, SALES, IMPORTATION, EXPORTATION)"),
    current_user: str = Depends(get_current_user)
):
    """
    Retorna o intervalo de anos disponíveis para o segmento especificado.
    """
    try:
        years = get_available_years(Segment.from_name(segment.upper()))
        
        if not years:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail = f"Não foram encontrados anos disponíveis para o segmento '{segment}'"
            )
        return years.to_dict()
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Erro ao obter anos para o segmento '{segment}': {str(e)}"
        )

@app.get("/products/{segment}")
async def get_products_by_segment_year_and_subOption(
    segment: str = Path(..., description = "Nome do segmento (PRODUCTION, PROCESSING, SALES, IMPORTATION, EXPORTATION)"),
    year: Optional[str] = Query(None, description = "Preencha com o ano que deseja obter os dados, deixe em branco para obter os dados do último ano"),
    sub_option: Optional[str] = Query(None, description = """
        Preencha com o sub option:

        **Para IMPORTATION ou EXPORTATION:**
        - TABLE_WINE (vinho de mesa)
        - SPARKLING_WINE (espumante)
        - FRESH_GRAPES (uvas frescas)
        - RAISINS (uvas passas)
        - GRAPE_JUICE (suco de uva)

        **Para PROCESSING:**
        - VINIFERA
        - AMERICAN_HYBRID
        - TABLE_GRAPE
        - UNCLASSIFIED
        """),
    current_user: str = Depends(get_current_user)
):
    """
    Retorna os dados de acordo com o segmento e ano desejado.
    """
    
    try:
        segment_enum = Segment.from_name(segment.upper())
        sub_option_enum = None
        
        if segment_enum == Segment.IMPORTATION or segment_enum == Segment.EXPORTATION:
            sub_option_enum = SubOption.from_name(sub_option.upper()) if sub_option else None
        
        if segment_enum == Segment.PROCESSING:
            sub_option_enum = ProcessingSubOption.from_name(sub_option.upper()) if sub_option else None
        
        products_data = get_products(segment_enum, year, sub_option_enum)
        
        if not products_data:
            raise HTTPException(
                status_code = status.HTTP_404_NOT_FOUND,
                detail = f"Não foram encontrados dados disponíveis para o segmento/ano '{segment}/{year}'"
            )
        return products_data
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail = f"Erro ao obter dados para o segmento/ano '{segment}/{year}': {str(e)}"
        )

if __name__ == "__main__":
    uvicorn.run("tech_challenge.api:app", host="0.0.0.0", port=8001, reload=True)
