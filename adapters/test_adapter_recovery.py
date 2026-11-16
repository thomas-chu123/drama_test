import sys, io, json, tempfile, os, importlib.util
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parent))
import comfyui_image_adapter as image
import comfyui_video_adapter as video
import comfyui_edit_adapter as edit
with patch.object(image.Path,'mkdir',side_effect=OSError('測試')):
    try: image.save_handle('/tmp/test-handle.json','original-id')
    except image.AdapterFailure as e: assert e.submitted and e.request_id=='original-id' and e.code=='handle_save_failed'
    else: raise AssertionError('未攔截保存錯誤')
job={'modality':'image','prompt':'測試','outputs':['test.png'],'output_root':'/tmp/adapter-fix-output'}
with patch.object(image,'read_job',return_value=job),patch.dict(os.environ,{'COMFYUI_TIMEOUT_SECONDS':'invalid'}),patch.object(image,'request_json') as request,patch('sys.stdout',new_callable=io.StringIO) as out:
    assert image.main()==1
    assert not request.called
    assert json.loads(out.getvalue())['error']['submitted'] is False
with tempfile.TemporaryDirectory() as d:
    with patch.object(video.urllib.request,'urlopen',side_effect=TimeoutError('測試')):
        try: video.download('http://localhost',None,{'filename':'test.mp4'},Path(d)/'test.mp4')
        except image.AdapterFailure as e: assert e.retryable and e.code=='download_failed'
        else: raise AssertionError('未攔截下載錯誤')
    for module,preflight in [(video,{'mode':'fl2va','timeout':1,'interval':.2}),(edit,({},Path('unused.png')))]:
        with patch.object(module,'preflight',return_value=preflight),patch.object(module,'get_history',side_effect=RuntimeError('測試')),patch.object(module,'request_json') as request:
            try: module.run({'collect_provider_job_id':'original-id'})
            except image.AdapterFailure as e: assert e.submitted and e.request_id=='original-id' and e.retryable
            else: raise AssertionError('未保留原任務編號')
            assert not request.called
print('adapter 離線回歸檢查通過')
