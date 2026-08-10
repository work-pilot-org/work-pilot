from fastapi import HTTPException
try:
    raise HTTPException(status_code=500, detail='Failed to create invitation in auth service.')
except HTTPException as e:
    print('Caught by HTTPException!')
except Exception as e:
    print('Caught by Exception!')
