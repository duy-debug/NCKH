"""
Routes cho hệ thống gợi ý kế hoạch học tập
"""

from flask import Blueprint, request, jsonify, current_app
from datetime import datetime

bp = Blueprint('recommendations', __name__, url_prefix='/api/recommendations')


@bp.route('', methods=['POST'])
def get_recommendation():
    """
    Tạo gợi ý kế hoạch học tập cho sinh viên
    
    Request:
    {
        "student_id": "SV0016",
        "custom_data": { ... }  # Tùy chọn
    }
    """
    try:
        # Kiểm tra hệ thống gợi ý đã sẵn sàng chưa
        if current_app.recommendation_engine is None:
            return jsonify({
                'success': False,
                'error': 'Hệ thống gợi ý chưa sẵn sàng. Vui lòng kiểm tra đường dẫn file ontology.',
            }), 500
        
        data = request.get_json()
        student_id = data.get('student_id', '').strip()
        
        if not student_id:
            return jsonify({
                'success': False,
                'error': 'student_id không được trống',
            }), 400
        
        # Lấy hồ sơ sinh viên
        student_service = current_app.student_data_service
        student = student_service.get_student(student_id)
        
        if not student:
            return jsonify({
                'success': False,
                'error': f'Không tìm thấy sinh viên {student_id}',
            }), 404
        
        # Kiểm tra dữ liệu sinh viên hợp lệ
        errors = student.validate()
        if errors:
            return jsonify({
                'success': False,
                'error': 'Dữ liệu sinh viên không hợp lệ',
                'details': errors,
            }), 400
        
        # Gọi hệ thống gợi ý
        engine = current_app.recommendation_engine
        result = engine.get_recommendation(student)
        
        # Gắn thời gian tạo
        result.generated_at = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'data': result.to_dict(),
        })
    
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        return jsonify({
            'success': False,
            'error': f'Lỗi xử lý: {str(e)}',
        }), 500

