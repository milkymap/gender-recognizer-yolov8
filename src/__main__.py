import click 

from .log import logger 
from .server import launch_server

@click.group()
@click.pass_context
def handler(ctx:click.core.Context):
    ctx.ensure_object(dict)

@handler.command()
@click.option('--host', type=str, default='0.0.0.0')
@click.option('--port', type=int, default=8000)
@click.option('--model_name', type=click.Path(exists=True, dir_okay=False))
@click.option('--mounting_path', type=str, default='/')
def deploy_server(host:str, port:int, model_name:str, mounting_path:str):
    try:
        launch_server(
            host=host,
            port=port,
            model_name=model_name,
            mounting_path=mounting_path
        ) 
    except KeyboardInterrupt:
        pass  
    except Exception as e:
        logger.error(e)

if __name__ == '__main__':
    handler()