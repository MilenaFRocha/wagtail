# Versão final para o arquivo: wagtail/tests/test_fields.py

import pytest
from django.db.models.fields import Field

from wagtail.blocks import CharBlock, StreamBlock
from wagtail.blocks.stream_block import StreamValue
from wagtail.fields import StreamField


class TestStreamFieldGetPrepValue:
    """
    Test the get_prep_value logic of the StreamField,
    specifically handling values with `raw_text`.
    """

    @pytest.fixture
    def stream_field(self):
        stream_block = StreamBlock([('text', CharBlock())])
        return StreamField(stream_block)

    def test_get_prep_value_when_stream_is_empty_with_raw_text_should_return_raw_text(self, stream_field):
        value = StreamValue(stream_field.stream_block, [], raw_text="raw text")
        result = stream_field.get_prep_value(value)
        assert result == "raw text"

    def test_get_prep_value_when_stream_is_empty_without_raw_text_should_delegate_to_stream_block(self, stream_field, mocker):
        value = StreamValue(stream_field.stream_block, [], raw_text=None)
        mock_block_prep = mocker.patch.object(stream_field.stream_block, 'get_prep_value')
        stream_field.get_prep_value(value)
        mock_block_prep.assert_called_once_with(value)

    def test_get_prep_value_when_stream_is_not_empty_should_delegate_to_stream_block(self, stream_field, mocker):
        value = StreamValue(stream_field.stream_block, [('text', 'Hi')])
        mock_block_prep = mocker.patch.object(stream_field.stream_block, 'get_prep_value')
        stream_field.get_prep_value(value)
        mock_block_prep.assert_called_once_with(value)

    def test_get_prep_value_when_value_is_not_stream_value_should_work_correctly(self, stream_field, mocker):
        """
        Test values that is not StreamValue should return the value directly and not call the StreamBlock's get_prep_value.
        """
        value = "any text"
        mock_block_prep = mocker.patch.object(stream_field.stream_block, "get_prep_value")

        result = stream_field.get_prep_value(value)
        mock_block_prep.assert_not_called()
        assert result == value